from google import genai
from google.genai import types
import time
import os
import json
import re
import logging


class GeminiClient:
    FALLBACK_MODELS = [
        "gemini-2.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-pro",
    ]

    def __init__(self, sys_instruct=None, model="gemini-2.5-flash", config=None, api_key=None):
        """初始化 GeminiClient 並設置 API 密鑰和系統指令

        :param sys_instruct: 系統指令
        :param model: 使用的模型名稱
        :param config: 生成內容的配置
        :param api_key: Gemini API 密鑰（如果為 None，將從環境變數讀取）
        """
        self.sys_instruct = sys_instruct
        self.model = model
        self.logger = logging.getLogger(__name__)
        self.config = config or types.GenerateContentConfig(
            system_instruction=sys_instruct,
            max_output_tokens=100,
            temperature=0.1
        )
        # 優先使用傳入的 api_key，否則從環境變數讀取
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please provide it via parameter or environment variable.")
        self.client = genai.Client(api_key=self.api_key)

    def _build_model_candidates(self, preferred_model=None):
        """
        構建模型候選清單，避免重複，並優先使用傳入/設定模型。
        """
        env_model = os.getenv("GEMINI_MODEL")
        candidates = [preferred_model, self.model, env_model, *self.FALLBACK_MODELS]
        ordered_candidates = []
        for item in candidates:
            if item and item not in ordered_candidates:
                ordered_candidates.append(item)
        return ordered_candidates

    def _is_not_found_error(self, error):
        """
        判斷是否屬於模型不可用（404/NOT_FOUND）錯誤。
        """
        message = str(error)
        return "404" in message or "NOT_FOUND" in message

    def _generate_content_with_fallback(self, contents, config=None, preferred_model=None):
        """
        逐個模型嘗試生成內容；若模型不可用則自動 fallback。
        """
        last_error = None
        for candidate_model in self._build_model_candidates(preferred_model):
            try:
                response = self.client.models.generate_content(
                    model=candidate_model,
                    contents=contents,
                    config=config or self.config,
                )
                if candidate_model != self.model:
                    self.logger.warning(
                        "Switched Gemini model from %s to %s due to model availability.",
                        self.model,
                        candidate_model,
                    )
                self.model = candidate_model
                return response
            except Exception as e:
                last_error = e
                if self._is_not_found_error(e):
                    self.logger.warning("Gemini model unavailable: %s", candidate_model)
                    continue
                raise

        raise last_error

    def generate_content(self, contents):
        """
        使用指定的模型和內容生成文本。

        :param contents: 要生成的內容
        :return: 生成的文本
        """
        response = self._generate_content_with_fallback(contents=contents)
        return response.text

    def _upload_file(self, file_name):
        """
        上傳文件並返回文件對象。

        :param file_name: 本地文件對象的名稱
        :return: 上傳的文件對象
        """
        print("Uploading file...")
        if file_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.mpg', '.webm', '.wmv', '.3gp')):
            file_path = os.path.join(os.path.dirname(__file__), 'static', 'video', file_name)
        else:
            file_path = os.path.join(os.path.dirname(__file__), 'static', 'image', file_name)
        uploaded_file = self.client.files.upload(file=file_path)
        print(f"Completed upload: {uploaded_file.uri}")
        return uploaded_file

    def _check_file_status(self, video_file):
        """
        檢查文件的處理狀態，直到文件處於 ACTIVE 狀態。

        :param video_file: 文件對象
        :return: 處於 ACTIVE 狀態的文件對象
        """
        while video_file.state.name == "PROCESSING":
            print('.', end='')
            time.sleep(1)
            video_file = self.client.files.get(name=video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(video_file.state.name)

        print('File is ready!')
        return video_file

    def _list_files(self):
        """
        列出所有上傳的文件及其 URI，並打印文件數量。

        :return: 文件名稱和 URI 的列表
        """
        files = self.client.files.list()
        file_list = [(f.name, f.uri) for f in files]
        print(f"Total number of files: {len(file_list)}")
        return file_list

    def evaluate_video(self, video_name):
        """
        使用指定的模型評價視頻。

        :param video_name: 視頻文件名稱
        :return: 生成的評價文本（已解析為 JSON 格式）
        """
        video_file = self._upload_file(video_name)
        video_file = self._check_file_status(video_file)
        response = self._generate_content_with_fallback(
            contents=[
                video_file,
                """
                You are a Japanese language master.
                Please evaluate the uploaded video based on the following criteria,
                and respond ONLY in JSON format, starts with '{' and ends with '}'.
                Limit "feedback_and_recommendations" text around 200 words,
                and with a more natural and conversational tone.
                Here is the response format:
                {
                "evaluation_criteria": {
                    "pronunciation_accuracy": {
                    "score": 1-10
                    },
                    "grammar_usage": {
                    "score": 1-10
                    },
                    "vocabulary_usage": {
                    "score": 1-10
                    },
                    "fluency": {
                    "score": 1-10
                    },
                    "comprehension": {
                    "score": 1-10
                    },
                    "jlpt_level": {
                    "score": "N1-N5"
                    }
                },
                "summary": {
                    "passing_probability": {
                    "N1": "1-100%",
                    "N2": "1-100%",
                    "N3": "1-100%",
                    "N4": "1-100%",
                    "N5": "1-100%"
                    },
                    "feedback_and_recommendations": "detailed feedback and recommendations"
                }
                }
                """
            ]
        )
        self._delete_file()  # Delete all uploaded files before returning
        return self._parse_handwriting_response(response.text)

    def transcribe_video(self, video_file):
        """
        轉錄視頻中的音頻，並提供時間戳和視覺描述。

        :param video_file: 視頻文件對象
        :return: 轉錄的文本和視覺描述
        """
        video_file = self._check_file_status(video_file)
        prompt = (
            "Transcribe the audio from this video, giving timestamps for "
            "salient events in the video. Also provide visual descriptions."
        )
        response = self._generate_content_with_fallback(contents=[video_file, prompt])
        return response.text

    def compare_handwriting(self, image_name, word):
        """
        比較手寫內容並生成描述。

        :param image_name: 圖片文件名稱
        :param word: 要比較的目標字符
        :return: 生成的描述文本（已解析為 JSON 格式）
        """
        image_file = self._upload_file(image_name)
        response = self._generate_content_with_fallback(
            contents=[
                image_file,
                f"""
                Compare the handwriting in this image with the Japanese character '{word}'.
                Respond ONLY in JSON format, starting with '{{' and ending with '}}'.
                Provide the following structure:
                {{
                    "similarity_score": {{
                        "score": 1-10
                    }},
                    "feedback": "Constructive feedback on how to improve the handwriting."
                }}
                """
            ]
        )
        self._delete_file()  # Delete all uploaded files before returning
        return self._parse_handwriting_response(response.text)

    def _parse_handwriting_response(self, response):
        """
        Parse the JSON part from the Gemini response text.
        """
        try:
            json_match = re.search(r'```json(.*?)```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1).strip())
            else:
                self.logger.error('No valid JSON found in the response')
                return None
        except Exception as e:
            self.logger.error(f'Error parsing handwriting response: {e}')
            return None

    def _delete_file(self):
        """
        刪除所有上傳的文件。
        """
        files = self._list_files()
        for file_name, _ in files:
            self.client.files.delete(name=file_name)
            print(f"Deleted file: {file_name}")


# Example usage
if __name__ == "__main__":
    gemini_client = GeminiClient()

    # Generate content example
    # result = gemini_client.generate_content(contents="講下JLPT")
    # print(result)

    # # Evaluate video example
    # evaluation = gemini_client.evaluate_video("test_video2.mp4")
    # print(evaluation)

    # Transcribe video example
    # transcription = gemini_client.transcribe_video(video_file)
    # print(transcription)

    # Compare handwriting example
    try:
        handwriting_result = gemini_client.compare_handwriting("handwriting.png", "さ")
        print(handwriting_result)
    except Exception as e:
        print(f"An error occurred while comparing handwriting: {e}")

    # Delete file example
    # try:
    #     gemini_client._delete_file()
    #     print("All files have been deleted successfully.")
    # except Exception as e:
    #     print(f"An error occurred while deleting files: {e}")

    # List files example
    # files = gemini_client._list_files()
    # for file_name, file_uri in files:
    #     print(f"File Name: {file_name}, File URI: {file_uri}")
