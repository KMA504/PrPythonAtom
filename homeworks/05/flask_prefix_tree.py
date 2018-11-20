from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

class PrefixTree:
    #TODO реализация класса prefix tree, методы как на лекции + метод дать топ 10 продолжений. Скажем на строку кросс выдаем кроссовки, кроссовочки итп. Как хранить топ? 
    #Решать вам. Можно, конечно, обходить все ноды, но это долго. Дешевле чуток проиграть по памяти, зато отдавать быстро (скажем можно взять кучу)
    #В терминальных (конечных) нодах может лежать json с топ актерами.
	###################################################################
	#Решение - использовать специальный метод для определения топ-10
    def __init__(self):
        self.root = [{}]
    
	#изменил метод add - добавил учёт частоты, если она передаётся вместо со строкой
    def add(self, string, freq=0):
        if self.check(string, freq):
            return
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                wrk_dict[0][i] = [{}]
                wrk_dict = wrk_dict[0][i]
        wrk_dict.append(True)
		#Помимо флага True добавляю следующим элементом в списке частоту.
        if freq>0:
            wrk_dict.append(freq)
        else:
            wrk_dict.append(1)
    
	#посчитал разумным увеличивать хранящуюся частоту слова, если оно приходит несколько раз
    def check(self, string, freq):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        if len(wrk_dict) != 1:
            if freq>0:
                wrk_dict[2]=wrk_dict[2]+freq
            else:
                wrk_dict[2]=wrk_dict[2]+1
            return True
        return False
    
    def check_part(self, string):
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        return True
    
	#метод определения частоты встречаемости - запрос перенаправляется во вспомогательный метод
	#Вспомогательный метод возвращает все возможные продолжения строки с их частотами
	#Затем эти строки сортируются сначала по частоте, а затем лексикографически. Затем уже выбирается топ-10.
    def continue10(self, request):
        res=[]
        fin=self.continue10main(request, res)
        if not fin:
            return fin
        fin2=pd.DataFrame(fin)
        fin3=fin2.sort_values([1, 0], ascending=[0, 1])
        return (fin3.head(10)[[0]].values.reshape(fin3.head(10)[[0]].values.shape[0])).tolist()
    
	#Метод, который проходит по дереву и фактически собирает все возможные продолжения слова.
	#Для охвата всех допустимых вариантов используется механизм рекурсии.
	#Допустимые варианты извлекаются вместе с их частотой встречаемости.
    def continue10main(self, request, res):
        wrk_dict = self.root
        if request[0] not in wrk_dict[0].keys():
            return res
        for i in request:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
        if len(wrk_dict)!=1:
            if wrk_dict[1]:
                if request not in res:
                    res.append([request, wrk_dict[2]])
        for j in wrk_dict[0].keys():
            self.continue10main(request+j, res=res)
        fin=res
        del res
        return fin

def init_prefix_tree(filename):
    #TODO в данном методе загружаем данные из файла. Предположим вормат файла "Строка, чтобы положить в дерево" \t "json значение для ноды" \t частота встречаемости
    ###################################################################
	#Не использовал json. Передаю в файле строки для вставки в дерево и частоту встречаемости.
	#Затем построчно вставляю каждую строку с её частотой в проинциализированное дерево.
	file=pd.read_csv(filename, delimiter='\t', encoding='cp1251', header=None)
	mass=np.array(file)
	pr_tree = PrefixTree()
	for i in range(mass.shape[0]):
		pr_tree.add(mass[i][0], mass[i][1])
	return pr_tree

@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    #TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод
	###################################################################
	#Инициализирую дерево файлом test.csv, лежащим в этой же папке.
	tree=init_prefix_tree('test.csv')
	result=tree.continue10(string)
	simp_dict={}
	simp_dict['sudgests']=result
	return json.dumps(simp_dict, ensure_ascii=False).encode('utf8')
	

@app.route("/")
def hello():
    #TODO должна возвращатьс инструкция по работе с сервером
	  return 'Сервер для поиска топ-10 саджестов. Введите /get_sudgest/string и на месте string укажите начало строки. Возвращается json, в котором по ключу suggests можно увидеть все подходящие саджесты.'

if __name__ == "__main__":
    app.run()
