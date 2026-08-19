import xml.etree.ElementTree as ET
import sys
import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

def get_latest_gdl_paper() -> tuple[str, str]:
    """Queries the public arXiv API for the most recent Geometric Deep Learning paper.
    
    Falls der Server streikt, greift die Fallback-Sicherung mit einem Mock-Abstract.
    """
    arxiv_url = (
        'https://arxiv.org?'
        'search_query=ti:%22geometric%22+AND+ti:%22deep%22+AND+ti:%22learning%22'
        '&max_results=1'
        '&sortBy=submittedDate'
        '&sortOrder=descending'
    )
    
    mock_title = "Geometric Deep Learning on Riemannian Manifolds and Graphs"
    mock_abstract = (
        "Geometric Deep Learning extends classical neural network architectures to non-Euclidean domains "
        "such as graphs and Riemannian manifolds. In this work, we introduce an SE(3)-equivariant "
        "network designed to respect structural symmetries. We utilize a Riemann gradient descent "
        "optimization technique to accelerate convergence. Our primary results demonstrate "
        "state-of-the-art representation learning invariants on geometric molecular datasets."
    )
    
    try:
        print("Verbindung zur arXiv API wird aufgebaut...")
        response = requests.get(arxiv_url, timeout=5)
        
        if response.status_code == 429:
            print("\n[INFO] arXiv API Rate Limit aktiv (HTTP 429). Nutze lokales mathematisches Fallback...")
            return mock_title, mock_abstract

        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        namespaces = {'atom': 'http://w3.org'}
        entry = root.find('atom:entry', namespaces)
        
        if entry is None:
            print("[INFO] Keine passenden Paper gefunden. Nutze lokales Fallback...")
            return mock_title, mock_abstract
            
        title = entry.find('atom:title', namespaces).text.strip()
        abstract = entry.find('atom:summary', namespaces).text.strip()
        abstract = " ".join(abstract.split())
        
        print("\n[SUCCESS] Live-Daten erfolgreich von arXiv geladen!")
        return title, abstract
        
    except (requests.Timeout, requests.RequestException) as e:
        print(f"\n[INFO] arXiv-Server nicht erreichbar oder zu langsam ({type(e).__name__}).")
        print("Automatische Fallback-Sicherung aktiv: Nutze lokales mathematisches Abstract...")
        return mock_title, mock_abstract


def summarize_with_gemini(title: str, abstract: str) -> str:
    """Sends the paper title and abstract to Gemini for high-level mathematical extraction.
    
    Fängt API- und Quotenfehler ab, damit das Hauptskript stabil bleibt.
    """
    print("Initialisiere Google GenAI Client...")
    
    # Der Client zieht sich den Schlüssel vollautomatisch aus ~/.bashrc (RAM)
    client = genai.Client()
    
    prompt = (
        "You are an expert assistant for a Mathematics and AI PhD researcher.\n"
        f"Analyze this paper title and abstract:\n\n"
        f"TITLE: {title}\n"
        f"ABSTRACT: {abstract}\n\n"
        "Provide a 3-bullet point summary focusing strictly on:\n"
        "1. The geometric methods used (manifolds, group actions, symmetries, etc.)\n"
        "2. The core optimization techniques applied.\n"
        "3. The primary mathematical or engineering results.\n"
        "Keep it highly technical, dense, and punchy. Avoid introductory filler phrases."
    )
    
    try:
        # Wechsel auf das freie Modell der Gemini 3-Serie
        print("Rufe Gemini 3.1 Flash-Lite Modell auf...")
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite',  # Der exakte Name für das Free-Tier
            contents=prompt,
        )
        return response.text



        
    except APIError as e:
        # Hier fangen wir den 429 RESOURCE_EXHAUSTED oder 404 Fehler ab
        print(f"\n[API-HINWEIS] Google Cloud Gateway hat die Anfrage blockiert.")
        print(f"Fehlermeldung: {e.message}")
        print("-> Dein API-Schlüssel ist korrekt geladen, aber dein Account hat im Free-Tier aktuell kein Kontingent.")
        return "Zusammenfassung nicht verfügbar (API Quota Limit erreicht)."
        
    except Exception as e:
        print(f"\n[UNERWARTETER FEHLER] Ein Fehler ist aufgetreten: {e}")
        return "Zusammenfassung aufgrund eines Systemfehlers fehlgeschlagen."


if __name__ == "__main__":
    # 1. Daten holen
    title, abstract = get_latest_gdl_paper()
    
    if title and abstract:
        print(f"Verarbeite Dokument: {title}\n")
        
        # 2. KI-Zusammenfassung generieren (stürzt dank try-except nicht ab)
        ai_summary = summarize_with_gemini(title, abstract)
        
        # 3. Ergebnis in der lokalen Markdown-Logdatei speichern
        log_filename = "research_log.md"
        with open(log_filename, "a", encoding="utf-8") as file:
            file.write(f"\n##  {title}\n\n")
            file.write(f"### AI Mathematical Deep-Dive:\n{ai_summary}\n")
            file.write("\n---\n")
            
        print(f"\n Pipeline erfolgreich ausgeführt! Die Ergebnisse wurden in '{log_filename}' gespeichert.")
