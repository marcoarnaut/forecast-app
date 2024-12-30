import requests
from bs4 import BeautifulSoup as bs

def load_data() -> dict:
    r = requests.get('https://www.yandex.com/weather/segment/details?offset=0&lat=55.753215&lon=37.622504&geoid=213&limit=10', headers = {'User-Agent':'Mozilla/5.0'}) 
    soup = bs(r.content, 'lxml')
    real_data = {}
    feelslike_data = {}
    for card in soup.select('.card:not(.adv)'):
        date = [i.text for i in card.select('[class$=number],[class$=month]')]
        if date != []:
            date[1] = date[1][:3]
            temps = list(zip([i.text for i in card.select('.weather-table__daypart')], [i.text for i in card.select('.weather-table__body-cell_type_daypart .temp__value')]))
            real_data[" ".join(date)] = temps
            temps = list(zip([i.text for i in card.select('.weather-table__daypart')], [i.text for i in card.select('.weather-table__body-cell_type_feels-like .temp__value')]))
            feelslike_data[" ".join(date)] = temps
            result = {"Real": real_data, "Feels like": feelslike_data}
    return result

def get_inp() -> list:
    inp: input = input("'Date' 'Month':")
    MONTHS: list = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    if len(inp.split(" ")) == 2:
        try:
            if isinstance(eval(inp.split(" ")[0]), int):
                if inp.split(" ")[1][:3].lower() in MONTHS:
                    return str(f"{eval(inp.split(" ")[0])} {inp.split(" ")[1][:3].title()}")
                print(f"Error: You must enter REAL month!")
                return get_inp()
            else:
                print(f"Error: You must enter INTEGER as date!")
                return get_inp()
        except Exception as e:
            print(f"Error: You must enter INTEGER as date!")
            return get_inp()
    else:
        print(f"Error: You must enter 'Date' and 'Month'!")
        return get_inp()
    
def get_data() -> list:
    def unpack_keys(li: list, before: str = "", after: str = "") -> str:
        try:
            result = ""
            for element in li:
                result += before + element + after
            return result[:len(result)-1]
        except:
            return None
    try:
        data = load_data()
        get = get_inp()
        result = []
        for element in list(data):
            result.append(data[element][get])
        return result
    except Exception as e:
        print(f"Error: Given date hasn't been determined, try again with another date. \n Determined dates: \n{unpack_keys([x for x in load_data()[list(load_data())[0]]], "\t", "\n")}")
        return False
    
def unpack_data(li: list, before: str = "", after: str = "") -> str:
    try:
        source = load_data()
        result = ""
        for element_idx in range(len(li)):
            result += f"{list(source)[element_idx]}:\n"
            for data in li[element_idx]:
                result += f"{before} {data[0]}: {data[1]} {after}"
        return result
    except:return None

def get_info() -> None:
    try:
        data = get_data()
        if data != False:
            return f"{unpack_data(data, "\t", "\n")}"
        raise Exception("Error with unpacking data")
    except Exception as e:
        return f"Unexcepted Error occured! \nError: {e}"


print(get_info())
# print(get_inp())