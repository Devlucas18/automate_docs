import unittest
import io
import os
import sys
from unittest.mock import MagicMock, patch
from PIL import Image

# Add the project root to sys.path so we can import 'service'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.imagem import imagem
from service.gerador import GeradorTermo

class TestImagemService(unittest.TestCase):
    def setUp(self):
        # Create a red 2000x2000 image in memory for testing
        self.fake_image = Image.new('RGB', (2000, 2000), color='red')

    def test_redimensionar(self):
        """Test if the image is resized to max 1280x720 maintaining aspect ratio."""
        processor = imagem(self.fake_image)
        # Access protected method directly for testing logic
        resized_img = processor._redimensionar(self.fake_image)
        
        self.assertLessEqual(resized_img.width, 1280)
        self.assertLessEqual(resized_img.height, 720)

    def test_process_returns_bytes(self):
        """Test if process returns bytes (JPEG data)."""
        processor = imagem(self.fake_image)
        result = processor.process()
        
        self.assertIsInstance(result, bytes)
        # Verify it is a valid image binary
        self.assertGreater(len(result), 0)


class TestGeradorTermoService(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "tipo_de_termo": "Notebook Recebimento",
            "nome": "Funcionario Teste",
            "cpf": "123.456.789-00",
            "img": "caminho/falso/foto.jpg"
        }

    def test_init_invalid_type(self):
        """Test initialization with an invalid document type."""
        invalid_data = {"tipo_de_termo": "Tipo Inexistente"}
        with self.assertRaises(ValueError):
            GeradorTermo(invalid_data)

    @patch("service.gerador.DocxTemplate")
    @patch("service.gerador.InlineImage")
    @patch("service.gerador.os.path.exists")
    @patch("service.gerador.Image.open")
    @patch("service.gerador.imagem")
    def test_gerar_doc_success(self, mock_imagem_cls, mock_img_open, mock_path_exists, mock_inline_image, mock_docxtpl):
        """Test the full flow of generating a document."""
        
        # 1. Setup Mocks
        mock_path_exists.return_value = True  # Pretend template file exists
        
        # Mock image processing
        mock_processor_instance = mock_imagem_cls.return_value
        mock_processor_instance.process.return_value = b"fake_image_bytes"
        
        # Mock DocxTemplate instance
        mock_doc_instance = mock_docxtpl.return_value

        # 2. Execute
        gerador = GeradorTermo(self.valid_data)
        gerador.gerar_doc()

        # 3. Assertions
        # Verify template existence check
        mock_path_exists.assert_called()
        
        # Verify image loading and processing
        mock_img_open.assert_called_with("caminho/falso/foto.jpg")
        mock_imagem_cls.assert_called()
        mock_processor_instance.process.assert_called()
        
        # Verify InlineImage was created (since we have an image)
        mock_inline_image.assert_called()
        
        # Verify document render and save
        mock_doc_instance.render.assert_called()
        # Check if save path matches the pattern in code
        expected_path = "gerados\\Termo_Notebook Recebimento_Funcionario_Teste.docx"
        mock_doc_instance.save.assert_called_with(expected_path)

    @patch("service.gerador.os.path.exists")
    def test_gerar_doc_template_not_found(self, mock_path_exists):
        """Test error when template file is missing."""
        mock_path_exists.return_value = False # Pretend file is missing
        
        gerador = GeradorTermo(self.valid_data)
        
        with self.assertRaises(FileNotFoundError):
            gerador.gerar_doc()

if __name__ == "__main__":
    unittest.main()
