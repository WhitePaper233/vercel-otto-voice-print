# coding: utf-8
import base64
import json
import os
import time
import uuid
import numpy as np
from pypinyin import lazy_pinyin
import soundfile as sf
import psola

class OTTO:
    def __init__(self, resource_path = './resources', target_sr = 44100) -> None:
        self.resource_path = resource_path
        self.target_sr = target_sr
        with open(f'{self.resource_path}/sentences/mapping.json', 'r', encoding='utf-8') as f:
            self.sentence_mapping = dict(json.load(f))
        with open(f'{self.resource_path}/words/mapping.json', 'r', encoding='utf-8') as f:
            self.word_mapping = dict(json.load(f))

    def loadAudio(self, related_file_path: str, normalizer: bool = True):
        data, sample_rate = sf.read(f'{self.resource_path}/{related_file_path}')
        # 双声道转单声道
        if len(data.shape) == 2:
            data = (data[:, 0] + data[:, 1]) / 2
        
        # 统一采样率
        if sample_rate != self.target_sr:
            new_lenth = int(len(data) * self.target_sr / sample_rate)
            data = np.interp(np.array(range(new_lenth)), np.linspace(0, new_lenth - 1, len(data)), data)

        # 标准化
        if normalizer:
            rms = np.sqrt(np.mean(data ** 2))
            data = data / rms * 0.2

        return data
    
    def modify_pitch_speed(self, data: np.array, pitch: float, speed: float):
        if pitch == 1.0 and speed == 1.0:
            return data

        # 防止音高过高或者速度过慢
        if pitch > 2.0 or speed < 0.5:
            return data
        
        # 音高变换
        if speed / pitch == 1.0:
            step1 = data
        else:
            step1 = psola.vocode(data, self.target_sr, constant_stretch=1/pitch)
            step1 = psola.vocode(step1, self.target_sr, constant_stretch=speed)
        
        # 速度变换
        new_length = int(len(data) / speed)
        return np.interp(np.array(range(new_length)), np.linspace(0, new_length - 1, len(step1)), step1)

    def generate(self, content: str, raw_sentence_mode: bool = True, pitch: float = 1.0, speed: float = 1.0, normalizer: bool = True):
        missing_words = []
        self.concatenated = np.array([])
        self.concatenated_audio = np.array([])

        content = content.lower()
        pronunciations = []

        # 切割句子
        splited_content = [[content, False]]
        if raw_sentence_mode:
            for sentence in self.sentence_mapping.items():
                i = 0
                while i < len(splited_content):
                    # 如果标记为原生大碟 则不进行切片
                    if splited_content[i][1]:
                        i += 1
                        continue
                    
                    if sentence[0] in splited_content[i][0]:
                        beginPosition = splited_content[i][0].index(sentence[0])
                        # 切割
                        splited_content.insert(i + 1, [splited_content[i][0][beginPosition:beginPosition + len(sentence[0])].strip(), True])
                        splited_content.insert(i + 2, [splited_content[i][0][beginPosition + len(sentence[0]):].strip(), False])
                        splited_content[i][0] = splited_content[i][0][:beginPosition].strip()
                    
                    i += 1

        # 根据映射表转换字符映射
        for i in range(len(splited_content)):
            pronunciations.append([])
            if splited_content[i][1]:
                pronunciations[i] = [self.sentence_mapping[splited_content[i][0]], True]
            else:
                pronunciations[i] = ["", False]
                for word in splited_content[i][0]:
                    if word in self.word_mapping:
                        pronunciations[i][0] += self.word_mapping[word] + ' '
                    else:
                        pronunciations[i][0] += word.strip() + ' '
        
        # 拼接音频
        for i in range(len(pronunciations)):
            if pronunciations[i][1]:
                try:
                    self.concatenated_audio = np.concatenate((self.concatenated_audio, self.loadAudio(f'sentences/{pronunciations[i][0]}.wav', normalizer)))
                except Exception:
                    if pronunciations[i][0] not in missing_words:
                        missing_words.append(pronunciations[i][0])
                        self.concatenated_audio = np.concatenate((self.concatenated_audio, np.zeros(int(self.target_sr/4))))
            
            else:
                pinyin = lazy_pinyin(pronunciations[i][0])
                for text in pinyin:
                    for word in text.split():
                        try:
                            self.concatenated_audio = np.concatenate((self.concatenated_audio, self.loadAudio(f'words/{word}.wav', normalizer)))
                        except Exception:
                            if word not in missing_words:
                                missing_words.append(word)
                                self.concatenated_audio = np.concatenate((self.concatenated_audio, np.zeros(int(self.target_sr/4))))

        # 音高变换
        self.concatenated_audio = self.modify_pitch_speed(self.concatenated_audio, pitch, speed)
    
    def export_file(self, file_path: str = './output.wav'):
        # 创建文件夹
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        # 导出文件
        sf.write(file_path, self.concatenated_audio, self.target_sr)


if __name__ == '__main__':
    otto = OTTO('../resources')
    otto.generate('大家好啊 我是一个好人 我是说的道理 哈哈哈哈 我是说的道理', raw_sentence_mode=True)
