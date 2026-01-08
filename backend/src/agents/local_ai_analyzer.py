"""
Ollama-based Local AI Analyzer
ローカルOllamaモデルを使用した翻訳・分析システム（Claude API代替）
"""
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import re

try:
    import ollama
except ImportError:
    raise ImportError("ollama package not installed. Run: pip install ollama")

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """分析結果データクラス"""
    original_text: str
    translated_text: Optional[str]
    sentiment: str  # positive, negative, neutral
    sentiment_score: float  # -1.0 to 1.0
    market_impact: str  # high, medium, low, none
    key_topics: List[str]
    summary: str
    analysis_timestamp: datetime
    model_used: str


class LocalAIAnalyzer:
    """
    Ollamaベースのローカル AI 分析システム

    使用モデル:
    - Qwen2.5 32B: 翻訳、詳細分析、要約 (高精度・やや低速)
    - Gemma 2 9B: センチメント分析 (高速・省メモリ)

    コスト削減:
    - Claude API: $7,880/月 → Ollama: 電気代のみ（$0/月）
    - 初期投資: RTX 4080 ($1,200) またはクラウドGPU ($130/月)
    """

    def __init__(
        self,
        main_model: str = "qwen2.5:32b",
        fast_model: str = "gemma2:9b",
        ollama_host: str = "http://localhost:11434"
    ):
        """
        Args:
            main_model: メインモデル（翻訳・分析用）
            fast_model: 高速モデル（センチメント分析用）
            ollama_host: Ollamaサーバーのホスト
        """
        self.main_model = main_model
        self.fast_model = fast_model
        self.ollama_host = ollama_host
        self.client = ollama.Client(host=ollama_host)

        # モデルが利用可能か確認
        self._check_models_availability()

    def _check_models_availability(self):
        """必要なモデルが利用可能か確認"""
        try:
            available_models = self.client.list()
            model_names = [m['name'] for m in available_models.get('models', [])]

            if self.main_model not in model_names:
                logger.warning(
                    f"Main model '{self.main_model}' not found. "
                    f"Run: ollama pull {self.main_model}"
                )

            if self.fast_model not in model_names:
                logger.warning(
                    f"Fast model '{self.fast_model}' not found. "
                    f"Run: ollama pull {self.fast_model}"
                )

            logger.info(f"Available models: {model_names}")

        except Exception as e:
            logger.error(f"Failed to connect to Ollama server: {e}")
            logger.error("Make sure Ollama is running: ollama serve")

    def translate_to_japanese(self, text: str, context: str = "") -> str:
        """
        英語テキストを日本語に翻訳

        Args:
            text: 翻訳するテキスト
            context: 追加のコンテキスト（投資・金融用語など）

        Returns:
            日本語翻訳
        """
        if not text or self._is_japanese(text):
            return text

        try:
            prompt = f"""以下の英語テキストを自然な日本語に翻訳してください。

【重要】
- 金融・投資用語は適切な日本語に翻訳
- 企業名、人名、固有名詞はそのまま残す
- 絵文字やハッシュタグはそのまま残す
- 自然で読みやすい日本語にする

{f'【コンテクスト】{context}' if context else ''}

【英語テキスト】
{text}

【日本語翻訳】
"""

            response = self.client.chat(
                model=self.main_model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.3,  # 低温度で正確な翻訳
                    'num_predict': 500,  # 最大トークン数
                }
            )

            translated = response['message']['content'].strip()
            logger.debug(f"Translated: {text[:50]}... -> {translated[:50]}...")

            return translated

        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text  # エラー時は元のテキストを返す

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        センチメント分析（高速モデル使用）

        Args:
            text: 分析するテキスト

        Returns:
            {
                'sentiment': 'positive' | 'negative' | 'neutral',
                'score': float (-1.0 to 1.0),
                'confidence': float (0.0 to 1.0)
            }
        """
        try:
            prompt = f"""以下のテキストのセンチメント（感情・トーン）を分析してください。

【分析対象テキスト】
{text}

【出力形式】
以下のJSON形式で出力してください：
{{
    "sentiment": "positive" または "negative" または "neutral",
    "score": -1.0から1.0の数値（-1.0=非常にネガティブ、0=中立、1.0=非常にポジティブ）,
    "confidence": 0.0から1.0の信頼度,
    "reasoning": "判定理由を1-2文で"
}}

JSONのみを出力してください："""

            response = self.client.chat(
                model=self.fast_model,  # 高速モデル使用
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.1,
                    'num_predict': 200,
                }
            )

            result_text = response['message']['content'].strip()

            # JSON抽出
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                logger.warning("Failed to parse sentiment JSON, using default")
                return {
                    'sentiment': 'neutral',
                    'score': 0.0,
                    'confidence': 0.5,
                    'reasoning': 'Parse error'
                }

        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'confidence': 0.0,
                'reasoning': f'Error: {str(e)}'
            }

    def analyze_market_impact(self, text: str, translated_text: str = "") -> Dict[str, Any]:
        """
        市場インパクト分析

        Args:
            text: 分析するテキスト（原文）
            translated_text: 翻訳済みテキスト（あれば）

        Returns:
            {
                'impact_level': 'high' | 'medium' | 'low' | 'none',
                'key_topics': List[str],
                'summary': str,
                'reasoning': str
            }
        """
        analysis_text = translated_text if translated_text else text

        try:
            prompt = f"""以下の投資・金融関連テキストの市場への影響度を分析してください。

【分析対象テキスト】
{analysis_text}

【分析項目】
1. 市場インパクトレベル（high/medium/low/none）
   - high: 市場を大きく動かす可能性のある重要情報
   - medium: 一部セクターや銘柄に影響する情報
   - low: 軽微な情報、参考程度
   - none: 市場への影響なし

2. キートピック（最大5個のキーワード）

3. 要約（1-2文）

【出力形式】
以下のJSON形式で出力してください：
{{
    "impact_level": "high" | "medium" | "low" | "none",
    "key_topics": ["トピック1", "トピック2", ...],
    "summary": "要約文",
    "reasoning": "インパクト判定の理由"
}}

JSONのみを出力してください："""

            response = self.client.chat(
                model=self.main_model,  # 詳細分析は高精度モデル使用
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.2,
                    'num_predict': 500,
                }
            )

            result_text = response['message']['content'].strip()

            # JSON抽出
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                logger.warning("Failed to parse market impact JSON, using default")
                return {
                    'impact_level': 'low',
                    'key_topics': [],
                    'summary': analysis_text[:100],
                    'reasoning': 'Parse error'
                }

        except Exception as e:
            logger.error(f"Market impact analysis failed: {e}")
            return {
                'impact_level': 'none',
                'key_topics': [],
                'summary': '',
                'reasoning': f'Error: {str(e)}'
            }

    def full_analysis(self, text: str, language: str = "unknown") -> AnalysisResult:
        """
        完全な分析パイプライン

        Args:
            text: 分析するテキスト
            language: テキストの言語 ("ja", "en", "unknown")

        Returns:
            AnalysisResult
        """
        logger.info(f"Starting full analysis (lang: {language})")

        # 1. 翻訳（英語の場合）
        translated_text = None
        if language == "en" or (language == "unknown" and not self._is_japanese(text)):
            logger.debug("Translating to Japanese...")
            translated_text = self.translate_to_japanese(text)

        # 2. センチメント分析（高速）
        logger.debug("Analyzing sentiment...")
        sentiment_result = self.analyze_sentiment(text)

        # 3. 市場インパクト分析
        logger.debug("Analyzing market impact...")
        impact_result = self.analyze_market_impact(text, translated_text or text)

        # 4. 結果を統合
        result = AnalysisResult(
            original_text=text,
            translated_text=translated_text,
            sentiment=sentiment_result.get('sentiment', 'neutral'),
            sentiment_score=sentiment_result.get('score', 0.0),
            market_impact=impact_result.get('impact_level', 'low'),
            key_topics=impact_result.get('key_topics', []),
            summary=impact_result.get('summary', ''),
            analysis_timestamp=datetime.now(),
            model_used=f"{self.main_model} + {self.fast_model}"
        )

        logger.info(
            f"Analysis complete: sentiment={result.sentiment}, "
            f"impact={result.market_impact}, topics={len(result.key_topics)}"
        )

        return result

    def _is_japanese(self, text: str) -> bool:
        """テキストが日本語かどうかを判定"""
        if not text:
            return False

        japanese_chars = sum(
            1 for char in text
            if '\u3040' <= char <= '\u309F' or  # ひらがな
               '\u30A0' <= char <= '\u30FF' or  # カタカナ
               '\u4E00' <= char <= '\u9FFF'     # 漢字
        )

        return (japanese_chars / len(text)) > 0.3 if len(text) > 0 else False


def main_test():
    """テスト用のメイン関数"""
    analyzer = LocalAIAnalyzer()

    # テスト1: 英語ツイート（翻訳 + 分析）
    english_tweet = """
    Breaking: Federal Reserve announces 25bps rate cut.
    This is the first rate cut in 4 years.
    Markets rally on the news. 📈 #Fed #RateCut
    """

    print("\n" + "="*80)
    print("Test 1: English Tweet Analysis")
    print("="*80)

    result = analyzer.full_analysis(english_tweet, language="en")

    print(f"\n【原文】\n{result.original_text}")
    print(f"\n【翻訳】\n{result.translated_text}")
    print(f"\n【センチメント】{result.sentiment} (スコア: {result.sentiment_score})")
    print(f"【市場インパクト】{result.market_impact}")
    print(f"【キートピック】{', '.join(result.key_topics)}")
    print(f"【要約】{result.summary}")

    # テスト2: 日本語ツイート（分析のみ）
    japanese_tweet = """
    日経平均が年初来高値を更新！
    半導体関連株が全面高。特にエヌビディアの決算を受けて
    国内半導体製造装置メーカーも急騰。🚀
    #日経平均 #半導体株
    """

    print("\n" + "="*80)
    print("Test 2: Japanese Tweet Analysis")
    print("="*80)

    result = analyzer.full_analysis(japanese_tweet, language="ja")

    print(f"\n【原文】\n{result.original_text}")
    print(f"【センチメント】{result.sentiment} (スコア: {result.sentiment_score})")
    print(f"【市場インパクト】{result.market_impact}")
    print(f"【キートピック】{', '.join(result.key_topics)}")
    print(f"【要約】{result.summary}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main_test()
