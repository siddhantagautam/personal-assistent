import pytest
import main

def test_speak_runs_without_error(monkeypatch):
    # monkeypatch tts engine
    monkeypatch.setattr(main.engine, "say", lambda text: None)
    monkeypatch.setattr(main.engine, "runAndWait", lambda: None)
    # should not raise
    main.speak("hello world")

def test_play_first_youtube_video_handles_no_match(monkeypatch):
    # monkeypatch requests.get to return text with no video url
    monkeypatch.setattr("main.requests.get", lambda url: type("R", (), {"text": "no matches here"})())
    called = {}
    monkeypatch.setattr(main, "speak", lambda t: called.setdefault("called", t))
    main.play_first_youtube_video("test query")
    assert called["called"] == "Video not found."

def test_processCommand_youtube_open(monkeypatch):
    opened = {}
    monkeypatch.setattr(main.web, "open", lambda url: opened.setdefault("url", url))
    monkeypatch.setattr(main, "play_first_youtube_video", lambda q: opened.setdefault("youtube", q))
    main.processCommand("play despacito on youtube")
    # Should call play_first_youtube_video
    assert "youtube" in opened

def test_processCommand_open(monkeypatch):
    called = {}
    monkeypatch.setattr(main.web, "open", lambda url: called.setdefault("url", url))
    monkeypatch.setattr(main, "speak", lambda t: None)
    main.processCommand("open facebook")
    assert "facebook.com" in called["url"]
