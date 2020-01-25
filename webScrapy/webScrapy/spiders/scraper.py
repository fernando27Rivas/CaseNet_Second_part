# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#from webScrapy.items import WebscrapyItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime, date, timedelta
import calendar
import csv
from selenium.webdriver.support.ui import Select
from .. import settings
from selenium.common.exceptions import NoSuchElementException

class ScraperSpider(CrawlSpider):
    name = 'scraper'
    allowed_domains = ['courts.mo.gov']
    search_url = 'https://www.courts.mo.gov/casenet/cases/calendarSearch.do'
    start_urls = ['https://www.courts.mo.gov/casenet/cases/calendarSearch.do']


    def parse(self, response):
        url = "https://www.courts.mo.gov/casenet/cases/calendarSearch.do"
        case_person=None
        first_name = ""
        last_name = ""
        first_name_def=""
        last_name_def=""
        addres_petitioner = ""
        city_petitioner = ""
        state_petitioner = ""
        zip_petitioner = ""
        city_descendent = ""
        addres_descendent = ""
        state_descendent = ""
        zip_descendent = ""
        save_csv=None
        fecha1 = date.today()  # Asigna fecha actual
        formato_fecha = "%d-%m-%Y"
        fecha_inicial = date.strftime(fecha1, formato_fecha)
        page_too=0
        count_page=1
        fecha2 = date.today() + timedelta(days=6)

        choice = settings.SELECT
        choice2 = settings.Judge
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")


        browser = webdriver.Chrome("C:/chromedriver.exe",chrome_options=options)
        #browser = webdriver.Chrome("/usr/local/bin/chromedriver")
        browser.get(url)
        time.sleep(4)
        
        select_box = Select(browser.find_element_by_id("courtId"))
        select_box.select_by_visible_text(choice)
        time.sleep(8)
        select2_box = Select(browser.find_element_by_id("JudgeId"))
        select2_box.select_by_visible_text(choice2)
        browser.find_element_by_css_selector("input#sevenDayRadio").click()
        browser.find_element_by_css_selector("input#judgeSortByPet").click()
        time.sleep(10)
        browser.find_element_by_id("findButton").click()
        time.sleep(3)



        try:
             time.sleep(8)
             pagination = browser.find_element_by_xpath("//tr[3]/td/table/tbody/tr[2]/td/form/table/tbody/tr").text
        except:
            pass
            pagination = browser.find_element_by_xpath("//tr[3]/td/table/tbody/tr[2]/td/form/table/tbody/tr").text
            print("Error en obtener la cantidad de paginas")


        pagination=pagination.split(" ")

        if(len(pagination)>10):
            for x in pagination:
                print("Numero de Pagina"+ str(x))


            hasNext=pagination[-4]
            print(hasNext)
            if (hasNext == "[Next"):
                last_page=pagination[-1]
                try:
                 last_page=last_page.split("]")[0]
                 print("Cantidad de Paginas mayor a 10")
                 if(int(last_page)>20):
                     print("Cantidad de Paginas mayor a 20")

                except:
                    pass
                    print("Cantidad de paginas menor a 10")
                    #last_page=pagination[-1]
        else:
            last_page = pagination[-1]





        print("LA ULTIMA PAGINA ES: "+str(last_page))


        try:
             initial_page=browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td/span").text
        except NoSuchElementException:
              pass
              time.sleep(2)
              initial_page = browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td/span").text

        initial_page=int(initial_page)



        while(count_page<=int(last_page)):
          print("Inicio de Pagina:" + str(count_page))

          if(initial_page!=1):
              try:
                   if (initial_page > 11):
                       if (count_page == 12):
                           initial_page=3
                       else:
                           if(count_page==22):
                              initial_page = 3
                           else:
                               if (count_page == 32):
                                   initial_page = 3
                               else:
                                   if (count_page == 42):
                                       initial_page = 3
                                   else:
                                       if (count_page == 52):
                                           initial_page = 3



                   print("Estamos en la pagina:" + str(count_page))
                   try:
                        browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td["+str(initial_page)+"]/a").click()
                   except NoSuchElementException:
                         pass
                         time.sleep(2)
                         browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td[" + str(initial_page) + "]/a").click()
              except NoSuchElementException:
                     pass
                     print("Error en la paginacion")

          #time.sleep(10)

          i=3

          while(i<=15):
            try :
                 time.sleep(10)
                 rest=browser.find_element_by_xpath("//tr["+str(i)+"]//td[contains(@class, 'td')][2]").text
            except NoSuchElementException:
                         pass
                         print("Error en la Busqueda de Elementos")
                         try:
                            time.sleep(8)
                            rest = browser.find_element_by_xpath(
                                "//tr[" + str(i) + "]//td[contains(@class, 'td')][2]").text

                         except NoSuchElementException:
                                print("'SALTO DE TABLA!!")
                                pass
                                if(i<15):
                                    i=i+2
                                    try:
                                        time.sleep(6)
                                        rest = browser.find_element_by_xpath(
                                            "//tr[" + str(i) + "]//td[contains(@class, 'td')][2]").text
                                    except NoSuchElementException:
                                        pass
                                        time.sleep(5)
                                        print("Final del Scraper")

                                else:
                                    print("Fin de Pagina.")


            if(rest is not None):

               print(rest)
               result= rest.split(' V ')
               print(result)
               for x in result:

                   result2 = x.split()
                   for rest_ind in result2 :
                       if(rest_ind== "LLC" or rest_ind=="INC"):
                           print("Se encontro un Caso de LLC o INC")
                           case_person=False
                       else:
                           case_person=True
                           print("Es un caso de Persona vrs Persona")

               if(case_person):

                    try:
                        time.sleep(6)
                        print("Busqueda de Numero de Caso")
                        browser.find_element_by_xpath("//tr[" + str(i) + "]//td[contains(@class, 'td')][1]/a").click()
                    except NoSuchElementException:
                        pass
                        time.sleep(5)
                        browser.find_element_by_xpath("//tr[" + str(i) + "]//td[contains(@class, 'td')][1]/a").click()
                        print("Error en Busqueda de Numero de Caso")


                    print("Busqueda de Tipo de Caso")
                    try:
                            time.sleep(3)
                            case = browser.find_element_by_xpath(
                                "//table[contains(@class,'detailRecordTable')]/tbody/tr[2]/td[4]").text
                            print("El tipo de caso es:" + str(case))
                    except:
                            pass
                            time.sleep(3)
                            print("Error in type case")
                    if(case== "AC Rent and Possession" or case== "Unlawful Detainer" or case=="AC Landlord Complaint"
                            or case=="AC Property Damage"):

                        try:
                            print("Entrando en los datos del caso")
                            browser.find_element_by_xpath("//tr/td/a/img[contains(@name,'parties')]").click()
                        except NoSuchElementException:
                            pass
                            print("Error in select a parties")
                            time.sleep(8)
                            browser.find_element_by_xpath("//tr/td/a/img[contains(@name,'parties')]").click()
                        p = 1
                        s = 0
                        while (p < 10):
                                try:
                                    time.sleep(10)
                                    print("Busqueda de Datos de Panfflit")
                                    result_path = browser.find_element_by_xpath(
                                        "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                            p) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                except NoSuchElementException:
                                    pass
                                    print("Error en Iteracion de variables P")

                                    try:
                                        time.sleep(10)
                                        print("Segundo Error en la Iteracion de Varble P")
                                        result_path = browser.find_element_by_xpath(
                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                p) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                    except NoSuchElementException:
                                        pass
                                        time.sleep(10)
                                        print("Tercer error de Iteracion en P")
                                        result_path = browser.find_element_by_xpath(
                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                p) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                p = p + 2
                                s = s + 2
                                print("El resultado de la path es:" + str(result_path))
                                res_petitioner = result_path.split(',')
                                first_name=res_petitioner[0]
                                last_name=res_petitioner[1]
                                print("El dato dividido  del Pannfitlit:")
                                print(res_petitioner)
                                for x in res_petitioner:
                                    temp = x.rstrip()
                                    temp = str(temp.lstrip())
                                    if("Plaintiff" in temp):
                                        print("Se encontro el Plaintiff")
                                        #Se procede a guardar los datos del Plaintiff
                                        try:
                                            time.sleep(10)
                                            petitioner_info = browser.find_element_by_xpath(
                                                "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                    s) + "]/td[contains(@class, 'detailData')][2]").text
                                        except NoSuchElementException:
                                            pass
                                            print("Error en obtener el Pettitioner")
                                        petitioner_split = petitioner_info.split(',')

                                        if (len(petitioner_info) > 1):

                                            var_city = 1
                                            var_temp = 1
                                            save_csv = True
                                            for x in petitioner_split:
                                                temp2 = x.rstrip()
                                                temp2 = temp2.lstrip()
                                                print("Data de Responsable en Iteracion:" + str(var_city))
                                                print(temp2)
                                                if (var_city == 1):
                                                    temp3 = temp2.split(sep="\n")
                                                    print("Valor de var_city: " + str(var_city))
                                                    for y in temp3:
                                                        print("Valor de Y en iteracion:" + str(var_temp))
                                                        if (var_temp == 1):
                                                            print(y)
                                                            addres_petitioner = y
                                                        else:
                                                            if (var_temp == 2):
                                                                print(y)
                                                                city_petitioner = y
                                                        var_temp = var_temp + 1
                                                else:
                                                    if (var_city == 2):
                                                        temp3 = temp2.split(sep="\n")
                                                        temp4 = list(filter(None, temp3))
                                                        var_temp3 = 1
                                                        if (var_temp3 == 1):
                                                            for z in temp4:
                                                                print("Iteracion Numero :" + str(var_temp3))
                                                                print("Valor temp4 separado " + str(z))
                                                                if (var_temp3 == 1):
                                                                    var_temp3 = var_temp3 + 1
                                                                    print("Primer valor de temp4: " + str(z))
                                                                    code = str(z)
                                                                    code = code.split()
                                                                    print("Valor de Code Separado:")
                                                                    print(code)
                                                                    value_q = 1
                                                                    for q in code:
                                                                        if (value_q == 1):
                                                                            print("Primer valor de Code:" + str(q))
                                                                            state_petitioner = q
                                                                            print("Estado del Petitioner: " + str(
                                                                                state_petitioner))
                                                                        else:
                                                                            if (value_q == 2):
                                                                                print("Segundo valor de Code:" + str(q))
                                                                                zip_petitioner = q
                                                                                print(
                                                                                    "Codigo Postal del Petitioner: " + str(
                                                                                        zip_petitioner))
                                                                        value_q = value_q + 1
                                                                        print(
                                                                            "Afuera de los if else el valor de Code es :" + str(
                                                                                q))

                                                        print("Valor de var_city en la Segunda Iteracion: " + str(
                                                            var_city))
                                                var_city = var_city + 1


                                        else:
                                            save_csv = False
                                        t = 1
                                        r = 0
                                        while (t < 10):
                                            try:
                                                decendent = browser.find_element_by_xpath(
                                                    "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                        t) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                            except NoSuchElementException:
                                                pass
                                                print("Error en Iteracion de variables T")
                                                try:
                                                    time.sleep(10)
                                                    decendent = browser.find_element_by_xpath(
                                                        "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                            t) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                                except NoSuchElementException:
                                                    pass
                                                    print("Segundo error de Iteracion en T")
                                                    time.sleep(10)
                                                    decendent = browser.find_element_by_xpath(
                                                        "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                            t) + "]/td[contains(@class, 'detailSeperator')][2]").text

                                            t = t + 2
                                            r = r + 2
                                            print(decendent)
                                            res_decendent = decendent.split(',')
                                            print("La Data del Defendent es")
                                            print(res_decendent)
                                            first_name_def = res_decendent[0]
                                            last_name_def = res_decendent[1]

                                            for x in res_decendent:
                                                temp = x.rstrip()
                                                temp = temp.lstrip()
                                                if (temp == "Defendant"):
                                                    print("Se encontro el Defendant")
                                                    print(temp)
                                                    t=11
                                                    p=11

                                                    try:
                                                        time.sleep(10)
                                                        decendet_info = browser.find_element_by_xpath(
                                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                                r) + "]/td[contains(@class, 'detailData')][2]").text
                                                    except NoSuchElementException:
                                                        pass
                                                        print("Error en obtener el Descendent")
                                                        time.sleep(5)
                                                        decendet_info = browser.find_element_by_xpath(
                                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                                r) + "]/td[contains(@class, 'detailData')][2]").text

                                                    decendent_split = decendet_info.split(",")

                                                    if (len(decendent_split) > 1):

                                                        var_city = 1
                                                        var_temp = 1
                                                        save_csv = True
                                                        for x in decendent_split:
                                                            temp2 = x.rstrip()
                                                            temp2 = temp2.lstrip()
                                                            print("Data de Responsable en Iteracion:" + str(var_city))
                                                            print(temp2)
                                                            if (var_city == 1):
                                                                temp3 = temp2.split(sep="\n")
                                                                print("Valor de var_city: " + str(var_city))
                                                                for y in temp3:
                                                                    print("Valor de Y en iteracion:" + str(var_temp))
                                                                    if (var_temp == 1):
                                                                        print(y)
                                                                        addres_descendent = y
                                                                    else:
                                                                        if (var_temp == 2):
                                                                            print(y)
                                                                            city_descendent = y
                                                                    var_temp = var_temp + 1
                                                            else:
                                                                if (var_city == 2):
                                                                    temp3 = temp2.split(sep="\n")
                                                                    temp4 = list(filter(None, temp3))
                                                                    var_temp3 = 1
                                                                    if (var_temp3 == 1):
                                                                        for z in temp4:
                                                                            print("Iteracion Numero :" + str(var_temp3))
                                                                            print("Valor temp4 separado " + str(z))
                                                                            if (var_temp3 == 1):
                                                                                var_temp3 = var_temp3 + 1
                                                                                print(
                                                                                    "Primer valor de temp4: " + str(z))
                                                                                code = str(z)
                                                                                code = code.split()
                                                                                print("Valor de Code Separado:")
                                                                                print(code)
                                                                                value_q = 1
                                                                                for q in code:
                                                                                    if (value_q == 1):
                                                                                        print(
                                                                                            "Primer valor de Code:" + str(
                                                                                                q))
                                                                                        state_descendent = q
                                                                                        print(
                                                                                            "Estado del Petitioner: " + str(
                                                                                                state_descendent))
                                                                                    else:
                                                                                        if (value_q == 2):
                                                                                            print(
                                                                                                "Segundo valor de Code:" + str(
                                                                                                    q))
                                                                                            zip_descendent = q
                                                                                            print(
                                                                                                "Codigo Postal del Petitioner: " + str(
                                                                                                    zip_descendent))
                                                                                    value_q = value_q + 1
                                                                                    print(
                                                                                        "Afuera de los if else el valor de Code es :" + str(
                                                                                            q))

                                                                    print(
                                                                        "Valor de var_city en la Segunda Iteracion: " + str(
                                                                            var_city))
                                                            var_city = var_city + 1


                                                    else:
                                                        save_csv = False





                                                    time.sleep(3)
                                                    browser.back()
                                                    browser.back()
                        if (save_csv):
                            with open('data.csv', 'a') as csvFile:
                                data_writer = csv.writer(csvFile)
                                data_writer.writerow([first_name, last_name, addres_petitioner, city_petitioner,
                                      state_petitioner, zip_petitioner,first_name_def,last_name_def
                                    , addres_descendent,city_descendent, state_descendent, zip_descendent, case])
                        else:
                            print("El elemento no se agrego Ya que no posee Suficientes datos.")
                        browser.back()



                    else:
                        print("No es el tipo de caso requerido")
                        time.sleep(3)
                        browser.back()
                        time.sleep(3)







               #Aumentamos Ya despues de Todas las Validaciones
               i=i+2
            else:
                i=i+2



          print("LLEGANDO A FIN DE LA PAGINA !!!")
          initial_page=initial_page+1
          count_page=count_page+1
          print("LA SIGUIENTE  PAGINA ES : " + str(count_page))





                       



        
        browser.close()


