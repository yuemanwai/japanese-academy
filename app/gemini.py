from google import genai
from google.genai import types
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self, sys_instruct):
        """初始化 GeminiClient 並設置 API 密鑰和系統指令"""
        self.sys_instruct = sys_instruct
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def generate_content(self, model, contents, config=None):
        """
        使用指定的模型和內容生成文本。

        :param model: 模型名稱
        :param contents: 要生成的內容
        :param config: 生成內容的配置（可選）
        :return: 生成的文本
        """
        response = self.client.models.generate_content(
            model=model, contents=contents, config=config
        )
        return response.text

    def upload_video(self, video_path):
        """
        上傳視頻文件並返回文件對象。

        :param video_path: 視頻文件的路徑
        :return: 上傳的文件對象
        """
        print("Uploading file...")
        video_file = self.client.files.upload(path=video_path)
        print(f"Completed upload: {video_file.uri}")
        return video_file

    def check_file_status(self, video_file):
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

    def summarize_video(self, video_file):
        """
        使用指定的模型生成視頻摘要和測驗。

        :param video_file: 視頻文件對象
        :return: 生成的摘要和測驗文本
        """
        response = self.client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[
                video_file,
                "Summarize this video. Then create a quiz with answer key "
                "based on the information in the video."
            ]
        )
        return response.text

    def transcribe_video(self, video_file):
        """
        轉錄視頻中的音頻，並提供時間戳和視覺描述。

        :param video_file: 視頻文件對象
        :return: 轉錄的文本和視覺描述
        """
        prompt = (
            "Transcribe the audio from this video, giving timestamps for "
            "salient events in the video. Also provide visual descriptions."
        )
        response = self.client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[video_file, prompt]
        )
        return response.text

    def list_files(self):
        """
        列出所有上傳的文件及其 URI。

        :return: 文件名稱和 URI 的列表
        """
        files = self.client.files.list()
        return [(f.name, f.uri) for f in files]

    def delete_file(self, file_name):
        """
        刪除指定名稱的文件。

        :param file_name: 文件名稱
        """
        self.client.files.delete(name=file_name)

# Example usage
if __name__ == "__main__":
    sys_instruct = "You are a cat. Your name is Neko."  # 替換為你的系統指令
    gemini_client = GeminiClient(sys_instruct)
    
    # Generate content example
    result = gemini_client.generate_content("gemini-2.0-flash", "講下JLPT",
    config=types.GenerateContentConfig(
        system_instruction=gemini_client.sys_instruct,
        max_output_tokens=100,
        temperature=0.1
    ))
    print(result)
    
    # Upload video example
    # video_file = gemini_client.upload_video("GreatRedSpot.mp4")
    
    # Check file status example
    # video_file = gemini_client.check_file_status(video_file)
    
    # Summarize video example
    # summary = gemini_client.summarize_video(video_file)
    # print(summary)
    
    # Transcribe video example
    # transcription = gemini_client.transcribe_video(video_file)
    # print(transcription)
    
    # List files example
    # files = gemini_client.list_files()
    # print('My files:')
    # for name, uri in files:
    #     print(f" {name}: {uri}")
    
    # Delete file example
    # gemini_client.delete_file(video_file.name)

