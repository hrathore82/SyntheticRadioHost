# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 20:28:06 2025

@author: Hemant S Rathore
"""

"""
Synthetic Radio Host - AI-Powered Audio Generation Tool

This script creates synthetic radio-style audio content by:
1. Fetching articles from Wikipedia based on user-provided topics
2. Converting English text into natural Hinglish (Hindi-English) conversations
   between two speakers using LLM (Ollama)
3. Generating high-quality audio using ElevenLabs text-to-speech API

Features:
- Supports both Streamlit web interface and CLI modes
- Uses Ollama LLM (default: llama3:8b) for Hinglish conversion
- Alternates between two different voices for realistic dialogue
- Includes audio cues like [happy], [laugh], [pause], etc. for natural expression
- Sanitizes and processes audio data for optimal quality

Requirements:
- Ollama running locally on port 11434
- ElevenLabs API key and voice IDs set as environment variables
- Required Python packages: nltk, langchain-ollama, wikipedia, elevenlabs, 
  numpy, soundfile, streamlit (optional), requests

Environment Variables:
- ELEVENLABS_API_KEY: Your ElevenLabs API key
- ELEVENLABS_voice_id_A: First voice ID for speaker A
- ELEVENLABS_voice_id_B: Second voice ID for speaker B

Usage:
    Streamlit Mode (stlit = True):
        streamlit run SyntheticRadioHost.py
        
    CLI Mode (stlit = False):
        python SyntheticRadioHost.py --text "Topic Name"
        
    Example:
        python SyntheticRadioHost.py --text "Artificial Intelligence"

Output:
    GeneratedAudio.wav - Final audio file saved in the script directory
"""

from nltk.tokenize import sent_tokenize
from langchain_ollama import OllamaLLM
import wikipedia as wiki
from datetime import datetime
from elevenlabs import ElevenLabs
import numpy as np
import soundfile as sf
import io,os,sys
import argparse
import requests

#*************** Update Value of stlit to True for running in Streamlit and False for running using CLI
stlit = True

LLM_Model = "llama3:8b"
import streamlit as st

def Ollama_Status():
    """
    Check if Ollama service is running and accessible on localhost.
    
    Attempts to connect to the Ollama API endpoint to verify the service
    is running. Uses a short timeout for quick response.
    
    Returns:
        bool: True if Ollama is running and accessible, False otherwise.
    """
    try:
        r = requests.get(
            "http://localhost:11434/api/tags",
            timeout=0.5   # very fast
        )
        return True
    
    except Exception as e:
        print("Ollama connection fail" + str(e))
        return False

def Conversation_Prompt():
    """
    Generate the system prompt for converting English text to Hinglish conversation.
    
    Creates a detailed prompt that instructs the LLM to convert English sentences
    into natural Hinglish dialogue between two speakers. The prompt includes
    guidelines for language style, grammar, fillers, and audio cues.
    
    Returns:
        str: A formatted prompt string containing instructions for Hinglish conversion.
    """
    prompt_Hinglish = """
Role: Expert Hinglish Scriptwriter specialized in natural, structured debates.

Task: Convert the provided English text into a fluid Hinglish discussion between two females speakers. The dialogue must be max 50–60 words.

Strict Guidelines:

Logical Flow: 
Dont use speaker names , just keep avoid it
Every turn must bridge from the previous statement . Ensure ideas evolve without repeating facts.
Language (Hinglish): Use Roman Hindi.
No English sentences. 
Blend English keywords (nouns/verbs) into Hindi grammar naturally.

Tone & Grammar:
Use Respectful plural forms.
Maintain strict noun-verb-gender agreement.

Fillers:
Include natural transitions like matlab, dekhiye, waise, sahi baat hai.

Audio Cues (ElevenLabs):
Use cues like [happy], [smile], [sad], [thinking], [sigh], [pause], [laugh], [serious], [relief], [excited], [surprised], [hmm], [clears throat].

Constraints:
1. START IMMEDIATELY: No intro, no "Here is the script," and no meta-tags.
2. Output should contain only conversation 
3. Strictly Avoid any Auto generated Note etc.
"""
    return prompt_Hinglish


def fetch_article_from_wiki(topic):
    """
    Fetch article summary from Wikipedia based on the given topic.
    
    Retrieves the first 500 characters of a Wikipedia article summary for the
    specified topic. The function handles input validation and error cases.
    
    Args:
        topic (str): The Wikipedia article topic to search for. Will be stripped
                     of leading/trailing whitespace.
    
    Returns:
        str or None: The first 500 characters of the article summary if successful,
                     None if the article cannot be found or an error occurs.
    """    
    topic = topic.lstrip()
    topic = topic.strip()
    
    if stlit:
        st.write(f"Article on {topic} fetching from wikipedia : {datetime.now().strftime("%H:%M:%S")}")
    print(f"Article on {topic} fetching from wikipedia : {datetime.now().strftime("%H:%M:%S")}")
    
    wiki.set_lang('en')
    
    if len(topic) > 0:
        try:
            data = wiki.page(topic, auto_suggest=False)
            
            if stlit:
                st.write((f"Article on {topic} Fetched from wikipedia : {datetime.now().strftime("%H:%M:%S")}"))
            print(f"Article on {topic} Fetched from wikipedia : {datetime.now().strftime("%H:%M:%S")}")
            
            return data.summary
        
        except Exception as ex:
            if stlit:
                st.error("Error in getting data from Wikipedia " +str(ex))
            print("Error in getting data from Wikipedia " +str(ex))
            return None
    else:
        print("Invalid/Empty article")
        if stlit:
            st.error("Invalid/Empty article")
        return None
    
def sentence_splitter(HinglishData):
    """
    Split Hinglish conversation data into separate sentences/lines.
    
    Processes the Hinglish conversation data by splitting on double newlines
    to separate individual dialogue lines or sentences. This prepares the
    data for audio generation where each line will be converted to speech.
    
    Args:
        HinglishData (list): A list of strings containing Hinglish conversation
                            data, typically from LLM output.
    
    Returns:
        list: A list of individual sentences/lines extracted from the input data.
              Returns an empty list if input is invalid or an error occurs.
    """
    sent_token=[]
    try:
        if len(HinglishData) < 1:
            if stlit:
                st.error("Invalid corpus: corpus must be a non-empty string")
            print("Error: Invalid corpus input")
            return []
        
        for line in HinglishData :
            Linesplit = line.split('\n\n')
            for line2 in Linesplit:
                sent_token.append(line2)
                      
        if stlit:
            st.write("Tokenization completed")
        print("Tokenization completed")  

        return sent_token
    
    except Exception as ex:
        if stlit:
            st.error(f"Error during tokenization: {str(ex)}")
        print(f"Tokenization error: {ex}")
        return []
    

def sentence_token(corpus):
    """
    Tokenize English text corpus into individual sentences.
    
    Uses NLTK's sentence tokenizer to split the input text into separate
    sentences. This is the first step in processing Wikipedia articles before
    converting them to Hinglish conversation.
    
    Args:
        corpus (str): The English text to tokenize. Must be a non-empty string.
    
    Returns:
        list: A list of sentence strings extracted from the corpus.
              Returns an empty list if input is invalid or an error occurs.
    
    Raises:
        Prints error messages to console and Streamlit (if enabled) but does not
        raise exceptions.
    """
    try:
        if corpus is None or not isinstance(corpus, str) or len(corpus.strip()) == 0:
            if stlit:
                st.error("Invalid corpus: corpus must be a non-empty string")
            print("Error: Invalid corpus input")
            return []
        
        corpus_token = sent_tokenize(corpus, language='english')
        print("Tokenization completed")
        if stlit:
            st.write("Tokenization completed")
        return corpus_token
    except Exception as ex:
        if stlit:
            st.error(f"Error during tokenization: {str(ex)}")
        print(f"Tokenization error: {ex}")
        return []    
    
def hinglish_converter(data):
    """
    Convert English sentences into Hinglish conversation using LLM.
    
    Takes a list of English sentences and converts each into natural Hinglish
    dialogue between two speakers using the Ollama LLM. The conversion follows
    the guidelines specified in Conversation_Prompt() to create conversational
    Hinglish text suitable for audio generation.
    
    Args:
        data (list): A list of English sentence strings to convert to Hinglish.
    
    Returns:
        list: A list of Hinglish conversation lines/sentences ready for audio
              generation. Each element represents dialogue that can be spoken.
    
    Note:
        - Uses the global LLM_Model variable (default: "llama3:8b")
        - Automatically splits the output using sentence_splitter()
    """
    
    llm = OllamaLLM(model=LLM_Model,temperature=0.35,top_p=0.9,top_k=40,repeat_penalty=1.18)
    HinglishData=[]
    
    if stlit:
        st.write("Hinglish conversion started : " + str(datetime.now().strftime("%H:%M:%S")))
    print("Hinglish conversation started : " + str(datetime.now().strftime("%H:%M:%S")))   
    
    prompt = Conversation_Prompt()
    
    if stlit:
        with st.spinner("Hinglish Conversion ongoing... please wait ⏳"):
            for sentence in data:
                Conversation=llm.invoke([{"role": "system", "content": prompt}, {"role": "user", "content": sentence}])
                HinglishData.append(Conversation)
    else:
        for sentence in data:
            Conversation=llm.invoke([{"role": "system", "content": prompt}, {"role": "user", "content": sentence}])
            HinglishData.append(Conversation)

    print("Hinglish conversion Done : " + str(datetime.now().strftime("%H:%M:%S")))
    if stlit:
        st.write("Hinglish conversion Done : " + str(datetime.now().strftime("%H:%M:%S")))

    Sent_token = sentence_splitter(HinglishData)
    return Sent_token


def sanitize_audio(audio_np):
    """
    Sanitize and normalize audio numpy array for processing.
    
    Processes raw audio data to ensure it's in the correct format for
    concatenation and file writing. Converts stereo to mono, handles edge
    cases like empty arrays or scalars, and reshapes to 1D array.
    
    Args:
        audio_np (numpy.ndarray or None): Raw audio data as numpy array.
                                         Can be mono or stereo, or None.
    
    Returns:
        numpy.ndarray or None: Sanitized 1D audio array ready for processing,
                              or None if input is invalid/empty.
    
    Processing:
        - Converts input to numpy array
        - Rejects scalar values (0-dimensional arrays)
        - Converts stereo (2D) to mono by averaging channels
        - Rejects empty arrays
        - Reshapes to 1D array
    """

    try:
        if audio_np is None:
            return None
        
        audio_np = np.asarray(audio_np)

        # Reject scalar
        if audio_np.ndim == 0:
            return None

        # Stereo → mono
        if audio_np.ndim == 2:
            audio_np = audio_np.mean(axis=1)

        # Reject empty
        if audio_np.size == 0:
            return None

        return audio_np.reshape(-1)
    except Exception as ex:
        print(f"Error sanitizing audio: {ex}")
        return None


def Get_Key_Env_varibles():
    """
    Retrieve ElevenLabs API credentials from environment variables.
    
    Fetches the required API key and voice IDs from environment variables.
    Exits the program if any required credentials are missing.
    
    Returns:
        tuple: A tuple containing (api_key, voice_id_A, voice_id_B) if all
               credentials are found.
    
    Environment Variables Required:
        - ELEVENLABS_API_KEY: ElevenLabs API key for authentication
        - ELEVENLABS_voice_id_A: First voice ID for speaker A
        - ELEVENLABS_voice_id_B: Second voice ID for speaker B
    
    Exits:
        sys.exit(0): If any required environment variable is missing.
    """
    # Get keys from environment
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print(" Eleven Labs API key Not available")
        sys.exit(0)
            
    voice_id_A = os.getenv("ELEVENLABS_voice_id_A")
    if not voice_id_A:
        print("1st Voice ID Not available")
        sys.exit(0)

    voice_id_B = os.getenv("ELEVENLABS_voice_id_B")
    if not voice_id_B:
        print("2nd Voice ID Not available")  
        sys.exit(0)
    return api_key ,voice_id_A , voice_id_B
    

def generate_audio(AudioData,Keys):
    """
    Generate audio file from Hinglish text using ElevenLabs TTS API.
    
    Converts a list of Hinglish conversation lines into speech using ElevenLabs
    text-to-speech API. Alternates between two different voices to create a
    realistic dialogue between two speakers. Combines all audio chunks into
    a single WAV file.
    
    Args:
        AudioData (list): A list of strings containing Hinglish conversation lines
                         to convert to speech. Each line will be spoken by
                         alternating voices.
        Keys (tuple): A tuple containing (api_key, voice_id_A, voice_id_B) from
                     Get_Key_Env_varibles().
    
    Returns:
        None: The function saves the audio file but doesn't return a value.
    
    Output:
        Creates "GeneratedAudio.wav" in the current working directory with:
        - Sample rate: 44100 Hz
        - Format: PCM_16 WAV
        - Mono audio (stereo converted to mono)
    """
    try:
        if not AudioData or len(AudioData) == 0:
            if stlit:
                st.error("Invalid audio data: must be a non-empty list")
            print("Error: Invalid AudioData input")
            return
        
        if stlit:
            st.write("Audio generation started : " + str(datetime.now().strftime("%H:%M:%S")))
        else:
            print("Audio generation started : " + str(datetime.now().strftime("%H:%M:%S")))

        try:
            client = ElevenLabs(api_key=Keys[0])
        except Exception as ex:
            if stlit:
                st.error(f"Failed to initialize ElevenLabs client: {str(ex)}")
            print(f"ElevenLabs initialization error: {ex}")
            return
        
        audio_chunks = []
        sample_rate = 44100
        VoiceID_Toggle=True
        for audioLine in AudioData:
            if VoiceID_Toggle :
                voice=Keys[1]
                speaker='Priya '
            else:
                voice=Keys[2]
                speaker='Kirti '
            try:
                audio_generator = client.text_to_speech.convert(
                    voice_id=voice,
                    text= speaker + str(audioLine),
                    voice_settings={
                        "stability": 0.5,
                        "similarity_boost": 0.6,
                        "style": 0.4,
                        "use_speaker_boost": True
                    },
                    model_id='eleven_v3')
             
                # toggleing voice ID's for using alternate voices
                if VoiceID_Toggle :
                    VoiceID_Toggle=False
                else:
                    VoiceID_Toggle=True
                
                audio_bytes = b"".join(chunk for chunk in audio_generator)
                
                if not audio_bytes:
                    print(f" Skipped empty audio chunk for voice {audioLine}")
                    continue
                
                audio_np, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32")
                audio_np = sanitize_audio(audio_np)

                if audio_np is None:
                    print(" Skipped invalid chunk")
                    continue
                
                audio_chunks.append(audio_np)
                print(f" Valid chunks: {len(audio_chunks)}")
                
            except Exception as ex:
                print(f" Error processing voice {audioLine}: {ex}")
                continue

        if not audio_chunks:
            if stlit:
                st.error("No valid audio chunks generated. Please check your API key and try again.")
            print("Error: No valid audio chunks to merge")
            return

        try:
            final_audio = np.concatenate(audio_chunks, axis=0)
            script_dir = os.getcwd()
            output_file = os.path.join(script_dir, "GeneratedAudio.wav")
            sf.write(output_file, final_audio, sample_rate, subtype="PCM_16")
            if stlit:
                st.write(f"Audio file generated {output_file}")
            else:
                print(f"Audio file generated {output_file}")
            
                
        except Exception as ex:
            if stlit:
                st.error(f"Error merging audio chunks: {str(ex)}")
            print(f"Error merging audio: {ex}")
            
    except Exception as ex:
        error_msg = f"Error in audio generation: {str(ex)}"
        
        if stlit:
            st.error(error_msg)
        print(error_msg)  
        
if stlit:
    if not Ollama_Status():
        sys.exit(0)
        
    st.title("Synthetic Radio Host tool")
    Name = st.text_input("Enter Article topic",max_chars=70)
    
    if st.button("Search"):
        try:
            if Name is not None and len(Name.strip()) > 2 and len(Name.strip()) < 71:
                corpus = fetch_article_from_wiki(Name)
               
                if corpus:
                    Corpus_token_full = sentence_token(corpus)
                    Corpus_token=[]
                    if len(Corpus_token_full)>5:
                        for i in range(5):
                            Corpus_token.append(Corpus_token_full[i])
                    else:
                        Corpus_token=Corpus_token_full
                    Sent_token = hinglish_converter(Corpus_token)
                    
                    # Get Environment keys
                    Keys = Get_Key_Env_varibles()
                    if Keys :
                        # generate Audio
                        generate_audio(Sent_token,Keys)
                        
                else:
                    st.error("Failed to fetch article. Please try a different topic.")
            else:
                st.warning("Please enter a valid article topic min 3 and max 70 Character")
        
        except Exception as ex:
            st.error(f"An unexpected error occurred: {str(ex)}")
            print(f"Unexpected error in main execution: {ex}")

else:           
    def main():
        """
        Main entry point for CLI mode execution.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("--text", required=True)
        args = parser.parse_args()
        if str(args.text) is not None and len(str(args.text).strip()) > 2 and len(str(args.text).strip())< 71:
            if not Ollama_Status():
                sys.exit(0)
                
            # fetching article from Wiki    
            corpus = fetch_article_from_wiki(str(args.text))
            if corpus:
                Corpus_token_full = sentence_token(corpus)
                Corpus_token=[]
                if len(Corpus_token_full)>5:
                    for i in range(5):
                        Corpus_token.append(Corpus_token_full[i])
                else:
                    Corpus_token=Corpus_token_full
                Sent_token = hinglish_converter(Corpus_token)
                
                # Get Environment keys
                Keys = Get_Key_Env_varibles()
                if Keys :
                    # generate Audio
                    generate_audio(Sent_token,Keys)

            else:
                print("Empty Output from Wiki")
        else:
            print("Please enter a valid article Name min 3 and max 70 Character")
    
    if __name__ == "__main__":
        main()

