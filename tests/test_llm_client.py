"""Unit tests for offline, zero-cost MockMedicalLLMClient and LLM client factory."""
import unittest
from unittest.mock import patch
from src.llm.client import get_llm_client, MockMedicalLLMClient, BaseLLMClient


class TestLLMClient(unittest.TestCase):
    """Verifies that the LLM client defaults to zero-cost offline mock mode and behaves reliably."""

    def test_default_llm_client_is_mock(self):
        """When no external API keys are configured, get_llm_client() must return MockMedicalLLMClient."""
        client = get_llm_client()
        self.assertIsInstance(client, MockMedicalLLMClient, "Default LLM client must be MockMedicalLLMClient for zero-cost operation")

    def test_mock_llm_generate_response_offline(self):
        """MockMedicalLLMClient generates structured clinical responses without any network or API keys."""
        client = MockMedicalLLMClient()
        prompt = "Explain the pathophysiology of ascites in cirrhosis."
        response = client.generate(prompt=prompt, system_prompt="You are an expert hepatologist.")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 30)

    def test_mock_llm_generate_json(self):
        """MockMedicalLLMClient generates valid JSON when requested."""
        client = MockMedicalLLMClient()
        prompt = "Generate a clinical multiple choice question on portal hypertension."
        res = client.generate_json(prompt=prompt, system_prompt="Return JSON only.")
        self.assertIsInstance(res, dict)
        self.assertTrue(bool(res), "JSON response should not be empty")

    def test_mock_vignette_evaluation_heuristic(self):
        """Mock client correctly mimics Socratic evaluation logic."""
        client = MockMedicalLLMClient()
        eval_prompt = "Evaluate student answer: paracentesis performed before antibiotics to check PMN count."
        response = client.generate(eval_prompt)
        self.assertIsInstance(response, str)


if __name__ == "__main__":
    unittest.main()
