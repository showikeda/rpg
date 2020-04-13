# 勇者 vs 魔王の1対1
# 魔王のとる行動は「攻撃」のみ
# 勇者のとれる行動は「攻撃」と「回復」の2択
# 行動順序は、各キャラの素早さに一定の乱数を掛けてソートさせることで決定する

from enum import Enum, auto
import random
import numpy as np  # NumPyは数値計算モジュール　npは変数名
# collections(コンテナデータ型)
# deque (両端における append や pop を高速に行えるリスト風のコンテナ)
# コンテナとは「複数のオブジェクトを格納できるオブジェクト」
# コンテナオブジェクトの例として、タプル、リスト、および辞書が挙げられます
# dequeについてのリンク↓
# https://docs.python.org/ja/3/library/collections.html#collections.deque
from collections import deque

class Character(object):

    """" キャラクタークラス　"""
    ACTIONS = {0: "攻撃", 1: "回復"}

    def __init__(self, hp, max_hp, attack, defence, agillity, intelligence, name):
        self.hp = hp  # 現在のHP
        self.max_hp = max_hp  # 最大HP
        self.attack = attack  # 攻撃力
        self.defence = defence  # 防御力
        self.agillity = agillity  # 素早さ
        self.intelligence = intelligence  # 賢さ
        self.name = name  # キャラクター

    # ステータス文字列を返す
    # returnについてのリンク
    # https://note.nkmk.me/python-function-def-return/
    def get_status_s(self):
        # ディクショナリー要素{}
        # formatの引数は{}の中に埋め込まれる、{}を連続で使用する場合は "/" で記入する
        # 例　HP:{}/{}　
        # https://qiita.com/Morio/items/b79ead5f881e6551d9e1
        # 出力の例 = [勇者] HP:20/20 ATK:4 DEF:1 AGO:5 INT:7
        return "[{}] HP:{}/{} ATK:{} DEF:{} AGO:{} INT:{}".format(
            self.name, self.hp, self.max_hp, self.attack, self.defence, self.agillity, self.intelligence)
    # def 関数名(self, 引数1, 引数2):
    # def action(勇者, 魔王, action):
    def action(self, target, action):

        # "0" = 攻撃
        if action == 0:

            # 攻撃力　- 防御力のダメージ計算
            # 機械学習に関する記事
            # https://employment.en-japan.com/engineerhub/entry/2018/11/09/110000
            # 多分self = 0, target = 1と考えたときに、[__init__キャラクター]の、勇者を０、魔王を１と関連付けできるのかも
            # だから0(勇者).attack, 1(魔王).defenceと考えられるのかも
            # 2[damage] = 4[hero] - 2[maou]
            damage = self.attack - target.defence
            draw_damage = damage  # ログ用

            # target.hp < damage : damageはtarget.hpより大きい
            # もし魔王HP < ダメージ[2]　ダメージが魔王HPより大きい時
            if target.hp < damage:
                damage = target.hp

            # ダメージを与える
            # target.hp[maou] = target.hp[maou] - damage[2]
            target.hp -= damage

            # 戦闘ログを返す
            return "{}は{}に{}のダメージを与えた".format(
               self.name, target.name, draw_damage)

        # "1" = 回復
        elif action == 1:

            # 回復量をINTの値とする
            heal_points = self.intelligence
            draw_heal_points = heal_points  # ログ用

            # self.hp + heal_points > self.max_hp
            # [self.hp + heal_points] は [self.max_hp] より大きい
            # もし　[勇者HP + 回復量]　は [勇者のMAX HP]　より大きい時
            # 回復量　は　勇者MAX HP - 現在の勇者HP　です
            if self.hp + heal_points > self.max_hp:
                heal_points = self.max_hp - self.hp

            # 回復
            # 勇者HP + 回復量　する
            self.hp += heal_points

            # 戦闘ログを返す
            return "{}はHPを{}回復した".format(
                self.name, draw_heal_points)

class GameState(Enum):

    # auto関数　=auto が使われている
    # https://qiita.com/gonemix/items/53f8601a023d509a59aa
    # ENUMの使い方が書かれている↑
    """" ゲーム状態管理クラス """
    TURN_START = auto()      # ターン開始　[1]
    COMMAND_SELECT = auto()  # コマンド選択 [2]
    TURN_NOW = auto()        # ターン中 (各キャラ行動) [3]
    TURN_END = auto()        # ターン終了 [4]
    GAME_END = auto()        # ゲーム終了 [5]

class Game():
    """" ゲーム本体 """
    HERO_MAX_HP = 20
    MAOU_MAX_HP = 50

    def __init__(self):

        # キャラクターを生成
        # self. __init__と関連付けされてる
        # 出力の例 = [勇者] HP:20/20 ATK:4 DEF:1 AGO:5 INT:7
        # hp, max_hp, attack, defence, agillity, intelligence, name
        # rand1 = random.randint(1,8)
        # rand2 = random.randint(1,8)
        # rand3 = random.randint(1,8)
        # rand4 = random.randint(1,8)
        #
        # rand5 = random.randint(1,8)
        # rand6 = random.randint(1,8)
        # rand7 = random.randint(1,8)
        # rand8 = random.randint(1,8)


        # heroint = [7, 10, 13, 15]
        # maouattack = [7, 10, 13, 15]

        # heroint = [1, 2, 3, 4]
        # maouattack =[1, 2, 3, 4]

        self.hero = Character(
            Game.HERO_MAX_HP, Game.HERO_MAX_HP, 5, 1, 5, 7, "勇者マサル")

        self.maou = Character(
            Game.MAOU_MAX_HP, Game.MAOU_MAX_HP, 5, 2, 6, 3, "魔王デスタムーア")


        # キャラクターリストに追加
        self.characters = []
        self.characters.append(self.hero)
        self.characters.append(self.maou)

        # 状態遷移用の変数を定義
        self.game_state = GameState.TURN_START

        # ターン数
        self.turn = 1

        # 戦闘ログを保存するための文字列
        self.log = ""

    # １ターン毎にゲームを進める
    def step(self, action):

        # メインループ
        while (True):
            if self.game_state == GameState.TURN_START:
                self.__turn_start()
            elif self.game_state == GameState.COMMAND_SELECT:
                self.__command_select(action)
            elif self.game_state == GameState.TURN_NOW:
                self.__turn_now()
            elif self.game_state == GameState.TURN_END:
                self.__turn_end()
                break  # ターン終了でもループを抜ける
            elif self.game_state == GameState.GAME_END:
                self.__game_end()
                break

        # ゲームが終了したかどうか
        done = False
        if self.game_state == GameState.GAME_END:
            done = True

        # 「状態s、報酬r、ゲームエンドかどうか」を返す
        return(self.hero.hp, self.maou.hp), self.reward, done

    # ゲームを１ターン目の状態に初期化
    def reset(self):
        self.__init__()
        return (self.hero.hp, self.maou.hp)

    # 戦闘ログを描画
    def draw(self):
        print(self.log, end="")

    def __turn_start(self):

        # 状態遷移
        self.game_state = GameState.COMMAND_SELECT

        # ログを初期化
        self.log = ""

        # 描画
        s = " *** ターン" + str(self.turn) + " ***"
        self.__save_log("\033[36m{}\033[0m".format(s))
        self.__save_log(self.hero.get_status_s())
        self.__save_log(self.maou.get_status_s())


    def __command_select(self, action):

        # 行動選択
        self.action = action

        # キャラクターを乱数0.5〜1.5の素早さ順にソートし、キューに格納
        self.character_que = deque(sorted(self.characters,
                                          key=lambda c: c.agillity*random.uniform(0.5, 1.5)))

        # 状態遷移
        self.game_state = GameState.TURN_NOW

        # ログ保存
        # 出力結果 = コマンド選択 -> 攻撃
        # 出力結果 = コマンド選択 -> 回復
        self.__save_log("コマンド選択 -> " + Character.ACTIONS[self.action])

    def __turn_now(self):

        # キャラクターキューから逐次行動
        if len(self.character_que) > 0:
            now_character = self.character_que.popleft()
            if now_character is self.hero:
                s = now_character.action(self.maou, self.action)
            elif now_character is self.maou:
                s = now_character.action(self.hero, action=0)  # 魔王は常に攻撃

            # ログを保存
            self.__save_log(s)

        # HPが0以下ならゲームエンド
        for c in self.characters:
            if c.hp <= 0:
                self.game_state = GameState.GAME_END
                return

        # 全員行動終了したらターンエンド
        if len(self.character_que) == 0:
            self.game_state = GameState.TURN_END
            return

    def __turn_end(self):

        # 報酬を設定
        self.reward = 0

        # キャラクターキューの初期化
        self.character_que = deque()

        # ターン経過
        self.turn += 1

        # 状態遷移
        self.game_state = GameState.TURN_START

    def __game_end(self):

        if self.hero.hp <= 0:
            self.__save_log("\033[31m{}\033[0m".format("勇者は死んでしまった"))
            self.reward = -1   # 報酬を設定
        elif self.maou.hp <= 0:
            self.__save_log("\033[32m{}\033[0m".format("魔王をやっつけた！"))
            self.reward = 1  # 報酬を設定

        self.__save_log("----ゲームエンド----")

    def __save_log(self, s):
        self.log += s + "\n"
