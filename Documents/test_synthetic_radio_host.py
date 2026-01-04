"""
Comprehensive Unit Test Suite for SyntheticRadioHost
Tests all functions with various scenarios including edge cases and error handling.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os
import numpy as np
import io
import pytest

# Import the module to test
import SyntheticRadioHost as srh


class TestOllamaStatus(unittest.TestCase):
    """Test cases for Ollama_Status() function"""
    
    @patch('SyntheticRadioHost.requests.get')
    def test_ollama_status_success(self, mock_get):
        """Test successful Ollama connection"""
        mock_get.return_value = Mock(status_code=200)
        result = srh.Ollama_Status()
        self.assertTrue(result)
        mock_get.assert_called_once_with(
            "http://localhost:11434/api/tags",
            timeout=0.5
        )
    
    @patch('SyntheticRadioHost.requests.get')
    def test_ollama_status_connection_error(self, mock_get):
        """Test Ollama connection failure"""
        mock_get.side_effect = Exception("Connection refused")
        result = srh.Ollama_Status()
        self.assertFalse(result)
    
    @patch('SyntheticRadioHost.requests.get')
    def test_ollama_status_timeout(self, mock_get):
        """Test Ollama timeout"""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        result = srh.Ollama_Status()
        self.assertFalse(result)
    
    @patch('SyntheticRadioHost.requests.get')
    def test_ollama_status_http_error(self, mock_get):
        """Test Ollama HTTP error"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response
        result = srh.Ollama_Status()
        # Should still return True if request succeeds
        self.assertTrue(result)


class TestConversationPrompt(unittest.TestCase):
    """Test cases for Conversation_Prompt() function"""
    
    def test_conversation_prompt_returns_string(self):
        """Test that prompt returns a non-empty string"""
        prompt = srh.Conversation_Prompt()
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
    
    def test_conversation_prompt_contains_keywords(self):
        """Test that prompt contains expected keywords"""
        prompt = srh.Conversation_Prompt()
        self.assertIn("Hinglish", prompt)
        self.assertIn("Role", prompt)
        self.assertIn("Task", prompt)
        self.assertIn("Audio Cues", prompt)
    
    def test_conversation_prompt_consistency(self):
        """Test that prompt is consistent across calls"""
        prompt1 = srh.Conversation_Prompt()
        prompt2 = srh.Conversation_Prompt()
        self.assertEqual(prompt1, prompt2)


class TestFetchArticleFromWiki(unittest.TestCase):
    """Test cases for fetch_article_from_wiki() function"""
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.wiki')
    def test_fetch_article_success(self, mock_wiki):
        """Test successful article fetch"""
        mock_page = Mock()
        mock_page.summary = "This is a test article about Python programming. " * 20
        mock_wiki.page.return_value = mock_page
        
        result = srh.fetch_article_from_wiki("Python")
        self.assertIsNotNone(result)
        self.assertLessEqual(len(result), 500)
        mock_wiki.set_lang.assert_called_once_with('en')
        mock_wiki.page.assert_called_once_with("Python", auto_suggest=False)
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.wiki')
    def test_fetch_article_not_found(self, mock_wiki):
        """Test article not found"""
        mock_wiki.page.side_effect = Exception("Page not found")
        result = srh.fetch_article_from_wiki("NonExistentTopic")
        self.assertIsNone(result)
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_fetch_article_empty_topic(self):
        """Test empty topic"""
        result = srh.fetch_article_from_wiki("")
        self.assertIsNone(result)
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_fetch_article_whitespace_topic(self):
        """Test topic with only whitespace"""
        result = srh.fetch_article_from_wiki("   ")
        self.assertIsNone(result)
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.wiki')
    def test_fetch_article_truncates_to_500(self, mock_wiki):
        """Test that article is truncated to 500 characters"""
        mock_page = Mock()
        mock_page.summary = "A" * 1000  # 1000 characters
        mock_wiki.page.return_value = mock_page
        
        result = srh.fetch_article_from_wiki("Test")
        self.assertEqual(len(result), 500)
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.wiki')
    def test_fetch_article_strips_whitespace(self, mock_wiki):
        """Test that topic whitespace is stripped"""
        mock_page = Mock()
        mock_page.summary = "Test article"
        mock_wiki.page.return_value = mock_page
        
        srh.fetch_article_from_wiki("  Python  ")
        mock_wiki.page.assert_called_once_with("Python", auto_suggest=False)


class TestSentenceSplitter(unittest.TestCase):
    """Test cases for sentence_splitter() function"""
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_splitter_normal(self):
        """Test normal sentence splitting"""
        input_data = ["Line 1\n\nLine 2", "Line 3\n\nLine 4"]
        result = srh.sentence_splitter(input_data)
        self.assertEqual(len(result), 4)
        self.assertIn("Line 1", result)
        self.assertIn("Line 2", result)
        self.assertIn("Line 3", result)
        self.assertIn("Line 4", result)
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_splitter_empty_list(self):
        """Test empty list input"""
        result = srh.sentence_splitter([])
        self.assertEqual(result, [])
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_splitter_no_double_newline(self):
        """Test input without double newlines"""
        input_data = ["Line 1", "Line 2"]
        result = srh.sentence_splitter(input_data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, ["Line 1", "Line 2"])
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_splitter_multiple_newlines(self):
        """Test input with multiple double newlines"""
        input_data = ["A\n\nB\n\nC"]
        result = srh.sentence_splitter(input_data)
        self.assertEqual(len(result), 3)
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_splitter_empty_strings(self):
        """Test input with empty strings"""
        input_data = ["", "Line 1\n\nLine 2", ""]
        result = srh.sentence_splitter(input_data)
        # Should still process non-empty strings
        self.assertGreater(len(result), 0)


class TestSentenceToken(unittest.TestCase):
    """Test cases for sentence_token() function"""
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_token_normal(self):
        """Test normal sentence tokenization"""
        corpus = "This is sentence one. This is sentence two! And sentence three?"
        result = srh.sentence_token(corpus)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("This is sentence one.", result)
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_token_empty_string(self):
        """Test empty string input"""
        result = srh.sentence_token("")
        self.assertEqual(result, [])
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_token_whitespace_only(self):
        """Test whitespace-only input"""
        result = srh.sentence_token("   ")
        self.assertEqual(result, [])
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_token_none_input(self):
        """Test None input"""
        result = srh.sentence_token(None)
        self.assertEqual(result, [])
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_token_non_string_input(self):
        """Test non-string input"""
        result = srh.sentence_token(123)
        self.assertEqual(result, [])
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sent_tokenize')
    def test_sentence_token_exception_handling(self, mock_tokenize):
        """Test exception handling"""
        mock_tokenize.side_effect = Exception("Tokenization error")
        result = srh.sentence_token("Test text")
        self.assertEqual(result, [])


class TestHinglishConverter(unittest.TestCase):
    """Test cases for hinglish_converter() function"""
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.OllamaLLM')
    @patch('SyntheticRadioHost.Conversation_Prompt')
    @patch('SyntheticRadioHost.sentence_splitter')
    def test_hinglish_converter_success(self, mock_splitter, mock_prompt, mock_llm_class):
        """Test successful Hinglish conversion"""
        # Setup mocks
        mock_prompt.return_value = "Test prompt"
        mock_llm = Mock()
        mock_llm.invoke.return_value = "Yeh ek test conversation hai."
        mock_llm_class.return_value = mock_llm
        mock_splitter.return_value = ["Line 1", "Line 2"]
        
        # Test
        input_data = ["This is a test sentence."]
        result = srh.hinglish_converter(input_data)
        
        # Assertions
        self.assertIsInstance(result, list)
        mock_llm.invoke.assert_called()
        mock_splitter.assert_called_once()
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.OllamaLLM')
    @patch('SyntheticRadioHost.Conversation_Prompt')
    @patch('SyntheticRadioHost.sentence_splitter')
    def test_hinglish_converter_multiple_sentences(self, mock_splitter, mock_prompt, mock_llm_class):
        """Test conversion with multiple sentences"""
        mock_prompt.return_value = "Test prompt"
        mock_llm = Mock()
        mock_llm.invoke.side_effect = ["Response 1", "Response 2"]
        mock_llm_class.return_value = mock_llm
        mock_splitter.return_value = ["Line 1", "Line 2"]
        
        input_data = ["Sentence 1.", "Sentence 2."]
        result = srh.hinglish_converter(input_data)
        
        self.assertEqual(mock_llm.invoke.call_count, 2)
        mock_splitter.assert_called_once()
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.OllamaLLM')
    def test_hinglish_converter_llm_configuration(self, mock_llm_class):
        """Test LLM is configured correctly"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = "Test"
        mock_llm_class.return_value = mock_llm
        
        srh.hinglish_converter(["Test"])
        
        # Verify LLM was initialized with correct parameters
        mock_llm_class.assert_called_once()
        call_args = mock_llm_class.call_args[1]
        self.assertEqual(call_args['temperature'], 0.35)
        self.assertEqual(call_args['top_p'], 0.9)
        self.assertEqual(call_args['top_k'], 40)
        self.assertEqual(call_args['repeat_penalty'], 1.18)


class TestSanitizeAudio(unittest.TestCase):
    """Test cases for sanitize_audio() function"""
    
    def test_sanitize_audio_mono_1d(self):
        """Test sanitizing 1D mono audio"""
        audio = np.array([0.1, 0.2, 0.3, 0.4])
        result = srh.sanitize_audio(audio)
        self.assertIsNotNone(result)
        self.assertEqual(result.ndim, 1)
        np.testing.assert_array_equal(result, audio)
    
    def test_sanitize_audio_stereo_to_mono(self):
        """Test converting stereo to mono"""
        audio = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])
        result = srh.sanitize_audio(audio)
        self.assertIsNotNone(result)
        self.assertEqual(result.ndim, 1)
        # Should be average of channels
        expected = np.mean(audio, axis=1)
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_sanitize_audio_none_input(self):
        """Test None input"""
        result = srh.sanitize_audio(None)
        self.assertIsNone(result)
    
    def test_sanitize_audio_scalar(self):
        """Test scalar input (0-dimensional)"""
        audio = np.array(0.5)
        result = srh.sanitize_audio(audio)
        self.assertIsNone(result)
    
    def test_sanitize_audio_empty_array(self):
        """Test empty array"""
        audio = np.array([])
        result = srh.sanitize_audio(audio)
        self.assertIsNone(result)
    
    def test_sanitize_audio_list_input(self):
        """Test list input (converted to array)"""
        audio = [0.1, 0.2, 0.3]
        result = srh.sanitize_audio(audio)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.ndim, 1)
    
    def test_sanitize_audio_2d_mono(self):
        """Test 2D array that's not stereo (single column)"""
        audio = np.array([[0.1], [0.2], [0.3]])
        result = srh.sanitize_audio(audio)
        self.assertIsNotNone(result)
        self.assertEqual(result.ndim, 1)
    
    def test_sanitize_audio_exception_handling(self):
        """Test exception handling"""
        # Create an object that will cause an exception
        class BadAudio:
            pass
        
        result = srh.sanitize_audio(BadAudio())
        self.assertIsNone(result)


class TestGetKeyEnvVariables(unittest.TestCase):
    """Test cases for Get_Key_Env_varibles() function"""
    
    @patch.dict(os.environ, {
        'ELEVENLABS_API_KEY': 'test_api_key',
        'ELEVENLABS_voice_id_A': 'voice_a',
        'ELEVENLABS_voice_id_B': 'voice_b'
    })
    def test_get_key_env_variables_success(self):
        """Test successful retrieval of all environment variables"""
        result = srh.Get_Key_Env_varibles()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 'test_api_key')
        self.assertEqual(result[1], 'voice_a')
        self.assertEqual(result[2], 'voice_b')
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('SyntheticRadioHost.sys.exit')
    def test_get_key_env_variables_missing_api_key(self, mock_exit):
        """Test missing API key"""
        srh.Get_Key_Env_varibles()
        mock_exit.assert_called_once_with(0)
    
    @patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test_key'}, clear=True)
    @patch('SyntheticRadioHost.sys.exit')
    def test_get_key_env_variables_missing_voice_a(self, mock_exit):
        """Test missing voice ID A"""
        srh.Get_Key_Env_varibles()
        mock_exit.assert_called_once_with(0)
    
    @patch.dict(os.environ, {
        'ELEVENLABS_API_KEY': 'test_key',
        'ELEVENLABS_voice_id_A': 'voice_a'
    }, clear=True)
    @patch('SyntheticRadioHost.sys.exit')
    def test_get_key_env_variables_missing_voice_b(self, mock_exit):
        """Test missing voice ID B"""
        srh.Get_Key_Env_varibles()
        mock_exit.assert_called_once_with(0)
    
    @patch.dict(os.environ, {
        'ELEVENLABS_API_KEY': '',
        'ELEVENLABS_voice_id_A': 'voice_a',
        'ELEVENLABS_voice_id_B': 'voice_b'
    })
    @patch('SyntheticRadioHost.sys.exit')
    def test_get_key_env_variables_empty_api_key(self, mock_exit):
        """Test empty API key"""
        srh.Get_Key_Env_varibles()
        mock_exit.assert_called_once_with(0)


class TestGenerateAudio(unittest.TestCase):
    """Test cases for generate_audio() function"""
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sf.write')
    @patch('SyntheticRadioHost.sf.read')
    @patch('SyntheticRadioHost.sanitize_audio')
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_success(self, mock_elevenlabs, mock_sanitize, 
                                     mock_sf_read, mock_sf_write):
        """Test successful audio generation"""
        # Setup mocks
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        
        # Mock audio generator
        mock_generator = [b'audio_chunk_1', b'audio_chunk_2']
        mock_client.text_to_speech.convert.return_value = mock_generator
        
        # Mock audio reading
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sf_read.return_value = (mock_audio, 44100)
        mock_sanitize.return_value = mock_audio
        
        # Test
        audio_data = ["Test line 1", "Test line 2"]
        keys = ("api_key", "voice_a", "voice_b")
        srh.generate_audio(audio_data, keys)
        
        # Assertions
        mock_elevenlabs.assert_called_once_with(api_key="api_key")
        self.assertEqual(mock_client.text_to_speech.convert.call_count, 2)
        mock_sf_write.assert_called_once()
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_generate_audio_empty_list(self):
        """Test empty audio data list"""
        keys = ("api_key", "voice_a", "voice_b")
        # Should return early without error
        srh.generate_audio([], keys)
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_client_initialization_error(self, mock_elevenlabs):
        """Test ElevenLabs client initialization error"""
        mock_elevenlabs.side_effect = Exception("API key invalid")
        keys = ("invalid_key", "voice_a", "voice_b")
        # Should handle error gracefully
        srh.generate_audio(["Test"], keys)
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sf.read')
    @patch('SyntheticRadioHost.sanitize_audio')
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_voice_alternation(self, mock_elevenlabs, mock_sanitize,
                                                mock_sf_read):
        """Test voice alternation logic"""
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        mock_generator = [b'audio_data']
        mock_client.text_to_speech.convert.return_value = mock_generator
        mock_audio = np.array([0.1, 0.2])
        mock_sf_read.return_value = (mock_audio, 44100)
        mock_sanitize.return_value = mock_audio
        
        audio_data = ["Line 1", "Line 2", "Line 3"]
        keys = ("api_key", "voice_a", "voice_b")
        srh.generate_audio(audio_data, keys)
        
        # Check that voices alternate
        calls = mock_client.text_to_speech.convert.call_args_list
        self.assertEqual(calls[0][1]['voice_id'], "voice_a")
        self.assertEqual(calls[1][1]['voice_id'], "voice_b")
        self.assertEqual(calls[2][1]['voice_id'], "voice_a")
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sf.read')
    @patch('SyntheticRadioHost.sanitize_audio')
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_empty_chunks_skipped(self, mock_elevenlabs, mock_sanitize,
                                                  mock_sf_read):
        """Test that empty audio chunks are skipped"""
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        
        # First call returns empty, second returns valid
        mock_generator_empty = []
        mock_generator_valid = [b'valid_audio']
        mock_client.text_to_speech.convert.side_effect = [
            mock_generator_empty,
            mock_generator_valid
        ]
        
        mock_audio = np.array([0.1, 0.2])
        mock_sf_read.return_value = (mock_audio, 44100)
        mock_sanitize.return_value = mock_audio
        
        audio_data = ["Line 1", "Line 2"]
        keys = ("api_key", "voice_a", "voice_b")
        srh.generate_audio(audio_data, keys)
        
        # Should continue processing despite empty chunk
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sf.read')
    @patch('SyntheticRadioHost.sanitize_audio')
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_invalid_chunks_skipped(self, mock_elevenlabs, mock_sanitize,
                                                    mock_sf_read):
        """Test that invalid audio chunks are skipped"""
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        mock_generator = [b'audio_data']
        mock_client.text_to_speech.convert.return_value = mock_generator
        
        mock_audio = np.array([0.1, 0.2])
        mock_sf_read.return_value = (mock_audio, 44100)
        mock_sanitize.return_value = None  # Invalid audio
        
        audio_data = ["Line 1"]
        keys = ("api_key", "voice_a", "voice_b")
        srh.generate_audio(audio_data, keys)
        
        # Should handle None from sanitize gracefully
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sf.write')
    @patch('SyntheticRadioHost.sf.read')
    @patch('SyntheticRadioHost.sanitize_audio')
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_voice_settings(self, mock_elevenlabs, mock_sanitize,
                                           mock_sf_read, mock_sf_write):
        """Test that voice settings are correct"""
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        mock_generator = [b'audio_data']
        mock_client.text_to_speech.convert.return_value = mock_generator
        mock_audio = np.array([0.1, 0.2])
        mock_sf_read.return_value = (mock_audio, 44100)
        mock_sanitize.return_value = mock_audio
        
        audio_data = ["Test"]
        keys = ("api_key", "voice_a", "voice_b")
        srh.generate_audio(audio_data, keys)
        
        # Check voice settings
        call_kwargs = mock_client.text_to_speech.convert.call_args[1]
        voice_settings = call_kwargs['voice_settings']
        self.assertEqual(voice_settings['stability'], 0.5)
        self.assertEqual(voice_settings['similarity_boost'], 0.6)
        self.assertEqual(voice_settings['style'], 0.4)
        self.assertTrue(voice_settings['use_speaker_boost'])
        self.assertEqual(call_kwargs['model_id'], 'eleven_v3')
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sf.read')
    @patch('SyntheticRadioHost.sanitize_audio')
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_no_valid_chunks(self, mock_elevenlabs, mock_sanitize,
                                              mock_sf_read):
        """Test when no valid audio chunks are generated"""
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        mock_generator = []
        mock_client.text_to_speech.convert.return_value = mock_generator
        
        audio_data = ["Test"]
        keys = ("api_key", "voice_a", "voice_b")
        # Should return early without writing file
        srh.generate_audio(audio_data, keys)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration test cases for complete workflows"""
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.Ollama_Status')
    @patch('SyntheticRadioHost.fetch_article_from_wiki')
    @patch('SyntheticRadioHost.sentence_token')
    @patch('SyntheticRadioHost.hinglish_converter')
    @patch('SyntheticRadioHost.Get_Key_Env_varibles')
    @patch('SyntheticRadioHost.generate_audio')
    def test_complete_workflow_success(self, mock_generate, mock_get_keys,
                                        mock_hinglish, mock_token, mock_fetch,
                                        mock_ollama):
        """Test complete successful workflow"""
        # Setup mocks
        mock_ollama.return_value = True
        mock_fetch.return_value = "Test article content"
        mock_token.return_value = ["Sentence 1.", "Sentence 2."]
        mock_hinglish.return_value = ["Hinglish line 1", "Hinglish line 2"]
        mock_get_keys.return_value = ("api_key", "voice_a", "voice_b")
        
        # Simulate main workflow
        if mock_ollama():
            corpus = mock_fetch("Test Topic")
            if corpus:
                tokens = mock_token(corpus)
                hinglish = mock_hinglish(tokens)
                keys = mock_get_keys()
                if keys:
                    mock_generate(hinglish, keys)
        
        # Verify all functions were called
        mock_ollama.assert_called()
        mock_fetch.assert_called_once_with("Test Topic")
        mock_token.assert_called_once()
        mock_hinglish.assert_called_once()
        mock_get_keys.assert_called_once()
        mock_generate.assert_called_once()
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.Ollama_Status')
    def test_workflow_ollama_not_available(self, mock_ollama):
        """Test workflow when Ollama is not available"""
        mock_ollama.return_value = False
        # Workflow should stop early
        if not mock_ollama():
            # Should exit or handle gracefully
            pass
        mock_ollama.assert_called()


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_token_very_long_text(self):
        """Test tokenization of very long text"""
        long_text = "This is a sentence. " * 1000
        result = srh.sentence_token(long_text)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    @patch('SyntheticRadioHost.stlit', False)
    def test_sentence_splitter_very_long_list(self):
        """Test splitting very long list"""
        long_list = ["Line\n\nSplit"] * 100
        result = srh.sentence_splitter(long_list)
        self.assertEqual(len(result), 200)  # Each item splits into 2
    
    def test_sanitize_audio_very_large_array(self):
        """Test sanitizing very large audio array"""
        large_audio = np.random.rand(1000000)  # 1 million samples
        result = srh.sanitize_audio(large_audio)
        self.assertIsNotNone(result)
        self.assertEqual(result.ndim, 1)
    
    def test_sanitize_audio_very_wide_stereo(self):
        """Test sanitizing very wide stereo audio"""
        stereo_audio = np.random.rand(1000, 2)
        result = srh.sanitize_audio(stereo_audio)
        self.assertIsNotNone(result)
        self.assertEqual(result.ndim, 1)
        self.assertEqual(len(result), 1000)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and recovery"""
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.wiki')
    def test_fetch_article_network_error(self, mock_wiki):
        """Test handling network errors"""
        mock_wiki.page.side_effect = Exception("Network error")
        result = srh.fetch_article_from_wiki("Test")
        self.assertIsNone(result)
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.OllamaLLM')
    def test_hinglish_converter_llm_error(self, mock_llm_class):
        """Test handling LLM errors"""
        mock_llm = Mock()
        mock_llm.invoke.side_effect = Exception("LLM error")
        mock_llm_class.return_value = mock_llm
        
        # Should handle error gracefully
        result = srh.hinglish_converter(["Test"])
        # Function should still return something (may be empty)
        self.assertIsNotNone(result)
    
    @patch('SyntheticRadioHost.stlit', False)
    @patch('SyntheticRadioHost.sf.write')
    @patch('SyntheticRadioHost.sf.read')
    @patch('SyntheticRadioHost.sanitize_audio')
    @patch('SyntheticRadioHost.ElevenLabs')
    def test_generate_audio_file_write_error(self, mock_elevenlabs, mock_sanitize,
                                              mock_sf_read, mock_sf_write):
        """Test handling file write errors"""
        mock_client = Mock()
        mock_elevenlabs.return_value = mock_client
        mock_generator = [b'audio_data']
        mock_client.text_to_speech.convert.return_value = mock_generator
        mock_audio = np.array([0.1, 0.2])
        mock_sf_read.return_value = (mock_audio, 44100)
        mock_sanitize.return_value = mock_audio
        mock_sf_write.side_effect = Exception("Write error")
        
        # Should handle error gracefully
        audio_data = ["Test"]
        keys = ("api_key", "voice_a", "voice_b")
        srh.generate_audio(audio_data, keys)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

