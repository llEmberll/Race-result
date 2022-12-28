import re
import json
import datetime as dtime
from datetime import datetime


def load_json(file_name):
    with open(file_name, encoding="utf8") as file:
        return json.load(file)


def get_results(file_name):
    results = {}

    re_for_number = r'([0-9]+)'
    re_for_time = r'([0-9]{2}:[0-9]{2}:[0-9]{2})'

    current_number = 0
    current_time = ''

    with open(file_name, encoding="utf8") as file:
        for element in file:
            record = element.strip()

            number = re.findall(re_for_number, record)[0]
            time = re.findall(re_for_time, record)[0]

            if current_number == number:                        #Если истина, значит указатель на строке с финишем
                time_difference = get_time_difference(current_time, time)
                results.update({number: int(time_difference.seconds)})
            else:
                current_number = number
                current_time = time
    return results


def get_time_difference(start, end):
    start = datetime.strptime(start, "%H:%M:%S")
    end = datetime.strptime(end, "%H:%M:%S")
    time_difference = end - start
    return time_difference


def set_placement(results):
    sorted_result = {k: results[k] for k in sorted(results, key=results.get, reverse=False)}
    return sorted_result


def get_time_from_sec(sec):
    time = str((dtime.timedelta(seconds=sec)))
    return time[2:]


def form_results_list(competitors, records):
    place = 1
    title = "   Занятое место    |  Нагрудной номер   |        Имя         |       Фамилия      |     Результат      "
    titles_len = 20
    titles_separator = ' '

    final_list = [title]

    for number in records:
        str_place = form_string(titles_len, titles_separator, str(place))
        str_number = form_string(titles_len, titles_separator, number)
        str_name = form_string(titles_len, titles_separator, competitors[number]['Surname'])
        str_surname = form_string(titles_len, titles_separator, competitors[number]['Name'])
        str_record = form_string(titles_len, titles_separator, get_time_from_sec(records[number]))

        str_competitor = f"{str_place}|{str_number}|{str_name}|{str_surname}|{str_record}"

        final_list.append(str_competitor)

        place += 1
    return final_list


def form_string(needle_len, separator, string):
    len_string = len(string)
    lens_difference = needle_len - len_string
    if lens_difference < 0:
        return string[0:needle_len-4]+'...'                     #Строка слишком длинная, нужно обрезать на 3 символа, чтобы вставить многоточие
    result_string = f"{string}" + separator*lens_difference
    return result_string


def main():
    competitors_info = load_json(r"competitors2.json")          #Загрузка входных данных относительным путем

    resutls_info = get_results(r"results_RUN.txt")

    sorted_result = set_placement(resutls_info)                 #Расстановка мест спортсменов с помощью сортировки их результатов по возрастанию

    res = form_results_list(competitors_info, sorted_result)    #Формирование строкового списка для удобного вывода

    print("\n".join(res))                                       #Красивый и ровный вывод результатов таблицей


main()

