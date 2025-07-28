from langchain_core.prompts import PromptTemplate
import re
from langchain_core.runnables import Runnable
import pyttsx3

def detect_intent(query:str, llm: any) -> str:
    """
    Detects the intent of user query
    
    Args: 
        query (str): User query in the form of a string
        llm (any): LLM object to use
    
    Return: 
        str: User intent categorized as a single word
    """
    from langchain_core.prompts import PromptTemplate

    intent_prompt = PromptTemplate.from_template(
        """
        You are an intent classifier for a virtual assistant. Categorize the user's request into one of the following intents:

        - calendar → anything involving scheduling, upcoming/past events, meetings, reminders, times, or dates
        - notes → anything about files, saved information, user thoughts, to-do lists, or written content
        - weather → anything about the weather, temperature, precipitation, etc.
        - general → casual conversation, questions, or anything that does not involve the calendar or notes

        Respond with only the intent keyword: calendar, notes, weather, or general.

        Examples:
        Query: What meetings do I have next week?  
        Intent: calendar

        Query: Add lunch with Sarah on Friday  
        Intent: calendar

        Query: Search my notes for project ideas  
        Intent: notes

        Query: What did I write about dreams last week?  
        Intent: notes

        Query: Tell me a joke  
        Intent: general

        Query: What’s the weather like today?  
        Intent: general

        Now classify this query:
        Query: {query}
        Intent:
        """
        )
    intent_chain: Runnable = intent_prompt | llm  # Using your OllamaLLM here
    try:
        result = intent_chain.invoke({"query": query})
        text = str(result).strip().lower()
        print(f"RESPONSE: {text}")
        # extract only calendar / notes / general using regex
        match = re.search(r"(calendar|notes|general|weather)", text)
        if match:
            return match.group(1)
        else:
            print("⚠️ Could not match intent, got:", text)
            return "general"

    except Exception as e:
        print("Intent detection failed, defaulting to general:", e)
        return "general"
    
# === TTS SETUP ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('voice', 'com.apple.voice.enhanced.en-ZA.Tessa')

def speak(text: str):
    """
    Speaks the text out loud via local speakers
    Args:
        text (str): Text to be read aloud
    """
    engine.say(text)
    engine.runAndWait()