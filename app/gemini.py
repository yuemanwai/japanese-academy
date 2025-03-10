from google import genai
from google.genai import types
import time
import os
from dotenv import load_dotenv
import json
import re 


# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self, sys_instruct=None, model="gemini-2.0-flash", config=None):
        """初始化 GeminiClient 並設置 API 密鑰和系統指令"""
        self.sys_instruct = sys_instruct
        self.model = model
        self.config = config or types.GenerateContentConfig(
            system_instruction=sys_instruct,
            max_output_tokens=100,
            temperature=0.1
        )
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def generate_content(self, contents):
        """
        使用指定的模型和內容生成文本。

        :param contents: 要生成的內容
        :return: 生成的文本
        """
        response = self.client.models.generate_content(
            model=self.model, contents=contents, config=self.config
        )
        return response.text

    def _upload_video(self, video_name):
        """
        上傳視頻文件並返回文件對象。

        :param video_path: 視頻文件的路徑
        :return: 上傳的文件對象
        """
        print("Uploading file...")
        video_path = f'/workspaces/FYP_AI-powered_Interactive_Japanese_Academy/app/static/video/{video_name}'
        video_file = self.client.files.upload(file=video_path)
        print(f"Completed upload: {video_file.uri}")
        return video_file

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

        print('Done')
        return video_file

    def _list_files(self):
        """
        列出所有上傳的文件及其 URI。

        :return: 文件名稱和 URI 的列表
        """
        files = self.client.files.list()
        return [(f.name, f.uri) for f in files]

    def evaluate_video(self, video_name):
        """
        使用指定的模型評價視頻。

        :param video_name: 視頻文件名稱
        :return: 生成的評價文本
        """
        files = self._list_files()
        video_file = next((f for f in files if f[0] == video_name), None)

        if not video_file:
            video_file = self._upload_video(video_name)
        else:
            video_file = self.client.files.get(name=video_file[0])

        video_file = self._check_file_status(video_file)
        response = self.client.models.generate_content(
            model=self.model,
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
        return response.text

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
        response = self.client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[video_file, prompt]
        )
        return response.text

    def delete_file(self, file_name):
        """
        刪除指定名稱的文件。

        :param file_name: 文件名稱
        """
        self.client.files.delete(name=file_name)


# Example usage
if __name__ == "__main__":
    gemini_client = GeminiClient()
    
    # Generate content example
    # result = gemini_client.generate_content(contents="講下JLPT")
    # print(result)
    
    # # Evaluate video example
    evaluation = gemini_client.evaluate_video("test_video2.mp4")
    # json_match = re.search(r'```json(.*?)```', evaluation, re.DOTALL)
    # if json_match:
    #     evaluation = json.loads(json_match.group(1).strip())  # Parse JSON response
    print(evaluation)
    
    # Transcribe video example
    # transcription = gemini_client.transcribe_video(video_file)
    # print(transcription)

    # Delete file example
    # gemini_client.delete_file(video_file.name)



