import unittest
import pandas as pd
from analise_dados import calcular_media

class TestAnalise(unittest.TestCase):
    def test_calcular_media(self):
        df = pd.DataFrame({"taxa_conversao": [0.1, 0.2, 0.3]})
        self.assertAlmostEqual(calcular_media(df), 0.2)

if __name__ == "__main__":
    unittest.main()
