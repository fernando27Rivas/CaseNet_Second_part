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
        fecha1 = date.today()  # Asigna fecha actual
        formato_fecha = "%d-%m-%Y"
        fecha_inicial = date.strftime(fecha1, formato_fecha)

        fecha2 = date.today() + timedelta(days=6)

        list_companys=["WELLS FARGO BANK","URBAN SOUTHWES","CELTIC PROPERTY MANAGEMENT","CROSSROADS OF LEES SUMMIT LIMITED PARTNERSHIP",
                       "GRAND BOULEVARD LOFTS LIMITED PARTNERSHIP","KC BUNGALOWS","MISSOURI DEPARTMENT OF REVENUE","STUDENT LOAN SOLUTIONS L"
                       ,"APEX SPECIALTY VEHICLES","ST. MARY'S MEDICAL CENTER","ST LUKES HOSPITAL OF K.C",
                       "ST. JOSEPH MEDICAL CENTER","UNIVERSITY OF KANSAS HEALT"," DIRECTOR OF REVENUE"]



        choice = settings.SELECT
        choice2 = settings.Judge
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--start-maximized")



        browser = webdriver.Chrome("C:/chromedriver.exe",chrome_options=chrome_options)
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
        except NoSuchElementException:
            pass
            print("Error en obtener la cantidad de paginas")
            try:

             pagination = browser.find_element_by_xpath("//tr[3]/td/table/tbody/tr[2]/td/form/table/tbody/tr").text
            except NoSuchElementException:
                print("Segundo Error en paginas")
                pass
                time.sleep(8)
                pagination = browser.find_element_by_xpath("//tr[3]/td/table/tbody/tr[2]/td/form/table/tbody/tr").text





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
              time.sleep(8)
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
                                           if(count_page==62):
                                               initial_page=3
                                           else:
                                                if(count_page==72):
                                                    initial_page=3
                                                else:
                                                    if(count_page==82):
                                                        initial_page=3
                                                    else:
                                                        if(count_page==92):
                                                            initial_page=3
                                                        else:
                                                            if(count_page==102):
                                                                initial_page=3


                   print("Estamos en la pagina:" + str(count_page))
                   try:
                        browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td["+str(initial_page)+"]/a").click()
                   except NoSuchElementException:
                         pass
                         time.sleep(8)
                         browser.find_element_by_xpath("//tr[8]/td/table/tbody/tr/td[" + str(initial_page) + "]/a").click()
              except NoSuchElementException:
                     pass
                     print("Error en la paginacion")



          i=3

          while(i<=15):
            try :
                 time.sleep(10)
                 rest=browser.find_element_by_xpath("//tr["+str(i)+"]//td[contains(@class, 'td')][2]").text
            except NoSuchElementException:
                         pass
                         print("Error en la Busqueda de Elementos")
                         try:
                            time.sleep(10)
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
                                        time.sleep(2)
                                        print("No se encontro Ningun Elemento")
                                        rest=None
                                        if(count_page==last_page):
                                            time.sleep(2)
                                            print("Final del Scraper")
                                            print("Se llego a la ultima pagina : " + str(last_page))
                                            browser.close()
                                else:
                                    i=16
                                    rest=None
                                    print("Fin de Pagina.")



            if(rest is not None):

               print(rest)
               result= rest.split(' V ')
               print(result)
               case_person = True
               for x in result:

                   result2 = x.split()
                   for rest_ind in result2 :
                       if("LLC" in rest_ind or  "INC" in rest_ind or "L .L.C." in rest_ind or "L.L." in rest_ind or "BANK" in rest_ind or "COMPANY" in rest_ind):
                           print("Se encontro un CASO de LLC o INC o un Banco")
                           case_person=False
                       else:
                           if("PARTNERSHIP" in rest_ind or "OF REVENUE" in rest_ind or "PROPERTY MANAGEMENT" in rest_ind or "KC BUNGALOWS" in rest_ind or
                           "STUDENT LOAN SOLUTIONS" in rest_ind or "MEDICAL CENTER" in rest_ind or "UNIVERSITY" in rest_ind or "URBAN SOUTHWES" in rest_ind
                           or "APEX SPECIALTY VEHICLES" in rest_ind or "CROSSROADS" in rest_ind or "CELTIC" in rest_ind):
                               case_person=False
                               print("Se encontro un valor en la Lista de Empresas")


               if(case_person):

                    try:
                        time.sleep(6)
                        print("Busqueda de Numero de Caso")
                        browser.find_element_by_xpath("//tr[" + str(i) + "]//td[contains(@class, 'td')][1]/a").click()
                    except NoSuchElementException:
                        pass
                        print("Error en Busqueda de Numero de Caso")
                        try:
                            time.sleep(10)
                            browser.find_element_by_xpath("//tr[" + str(i) + "]//td[contains(@class, 'td')][1]/a").click()
                        except NoSuchElementException:
                            time.sleep(8)
                            browser.find_element_by_xpath(
                                "//tr[" + str(i) + "]//td[contains(@class, 'td')][1]/a").click()
                            print(" Segundo Error en Busqueda de Numero de Caso")
                    #Ya se Ingreso a el codigo de caso se muestra el tipo de caso (Solo es necesario un back() para regresar


                    print("Busqueda de Tipo de Caso")
                    try:
                            time.sleep(8)
                            case = browser.find_element_by_xpath(
                                "//table[contains(@class,'detailRecordTable')]/tbody/tr[2]/td[4]").text
                            print("El tipo de caso es:" + str(case))
                    except NoSuchElementException:
                            pass
                            print("Error in type case")
                            time.sleep(8)
                            try:
                                case = browser.find_element_by_xpath(
                                    "//table[contains(@class,'detailRecordTable')]/tbody/tr[2]/td[4]").text
                                print("El tipo de caso es:" + str(case))
                            except NoSuchElementException:
                                pass
                                print("Segundo Error en tipo de Caso")
                                time.sleep(8)
                                case = browser.find_element_by_xpath(
                                    "//table[contains(@class,'detailRecordTable')]/tbody/tr[2]/td[4]").text
                                print("El tipo de caso es:" + str(case))
                                try:
                                   time.sleep(8)
                                   case = browser.find_element_by_xpath(
                                       "//table[contains(@class,'detailRecordTable')]/tbody/tr[2]/td[4]").text
                                except NoSuchElementException:
                                   pass
                                   print("No mames Ya encuentralo")
                                   time.sleep(3)
                                   case = browser.find_element_by_xpath(
                                    "//table[contains(@class,'detailRecordTable')]/tbody/tr[2]/td[4]").text
                # Ya se capturo el tipo de Caso y se procede a validar que sea de los 4 requeridos

                # Es del Tipo de caso que necesitamos
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
                 #Entramos en la seccion donde vamos a Scrapear los datos
            # Ya se necesitan dos back() para regresar


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
                                panfit_doe=True
                                if("JOHN" in res_petitioner[0] and "DOE" in res_petitioner[1]):
                                    panfit_doe=False
                                    print("Es un JOHN DOE")
                                else:
                                    if("JANE" in res_petitioner[0] and "DOE" in res_petitioner[1]):
                                        panfit_doe=False
                                        print("ES una JANE DOE")


                    # Ya tenemos el Plaintiff y procedemos a revisar si Contiene los caracteres LLC o INC
                                print(res_petitioner)
                     #Asumimos inicialmente que si es una persona
                                pantf_person=True
                                for g in res_petitioner:
                                    if ( "LLC" in g or "INC" in g or "L .L.C." in g or "L.L." in g or "BANK" in g or "COMPANY" in g ):
                                        pantf_person=False
                                        print("El panflit es un LLC o una INC o Una COmpaNy o UN BANK.")
                                    else:
                                        if ("PARTNERSHIP" in g or "OF REVENUE" in g or "PROPERTY MANAGEMENT" in g or "KC BUNGALOWS" in g or
                                        "STUDENT LOAN SOLUTIONS" in g or "MEDICAL CENTER" in g or "UNIVERSITY" in g or "URBAN SOUTHWES" in g
                                        or "APEX SPECIALTY VEHICLES" in g or "CROSSROADS" in g or "CELTIC" in g):
                                            pantf_person = False
                                            print("El panflit pertenece a la lista de empresas.")


                    #Ya se recorrio el Plaintiff y si contiene la cadena LLC o INC

                                if(pantf_person ):
                                    if(panfit_doe):
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
                                                        petitioner_info=None
                                                    if(petitioner_info):
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
                                                        control=0
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
                                                                    try:
                                                                        decendent = browser.find_element_by_xpath(
                                                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                                                t) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                                                    except NoSuchElementException:
                                                                        decendent=None
                                                                        pass
                                                                        print("No se encontro un resultado")
                                                                        control=control+1
                                                                if(control==2):
                                                                    t=t+1
                                                                    try:
                                                                        time.sleep(10)
                                                                        decendent = browser.find_element_by_xpath(
                                                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table// tr[" + str(
                                                                                t) + "]/td[contains(@class, 'detailSeperator')][2]").text
                                                                    except NoSuchElementException:
                                                                        pass
                                                                        print("Tercer error de Iteracion en T")

                                                            if(decendent is not None):
                                                                t = t + 2
                                                                r = r + 2
                                                                print(decendent)
                                                                res_decendent = decendent.split(',')
                                                                print("La Data del Defendent es")
                                                                print(res_decendent)
                                                                decendent_person=True
                                                                for x in res_decendent:
                                                                    if("LLC" in x or "INC" in x):
                                                                        decendent_person=False


                                                                if(decendent_person):
                                                                    for x in res_decendent:
                                                                        temp = x.rstrip()
                                                                        temp = temp.lstrip()
                                                                        if (temp == "Defendant"):
                                                                            print("Se encontro el Defendant")
                                                                            print(temp)
                                                                            t=11
                                                                            p=11
                                                                            control_r=0
                                                                            while(r<=10):

                                                                                try:
                                                                                    time.sleep(10)
                                                                                    decendet_info = browser.find_element_by_xpath(
                                                                                        "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                                                            r) + "]/td[contains(@class, 'detailData')][2]").text
                                                                                except NoSuchElementException:
                                                                                    pass
                                                                                    print("Error en obtener el Descendent")
                                                                                    time.sleep(8)
                                                                                    try:
                                                                                        decendet_info = browser.find_element_by_xpath(
                                                                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                                                                r) + "]/td[contains(@class, 'detailData')][2]").text
                                                                                    except NoSuchElementException:
                                                                                        pass
                                                                                        print("Error en obtener a data")
                                                                                        control_r=control_r+1
                                                                                        decendet_info=None
                                                                                if(control_r==2):
                                                                                    r=r+1
                                                                                    try:
                                                                                        decendet_info = browser.find_element_by_xpath(
                                                                                            "//table[contains(@class, 'outerTable')]//td[contains(@valign, 'top')]/form/table//tr[" + str(
                                                                                                r) + "]/td[contains(@class, 'detailData')][2]").text
                                                                                    except NoSuchElementException:
                                                                                        pass
                                                                                        print("Error en obtener a data")






                                                                                if(decendet_info is not None):
                                                                                    r=11
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
                                                                                else:
                                                                                    print("Valor nulo de datos de Defendant")
                                                                                    r=r+2

                                                                else:
                                                                    print("EL Dedendent no era persona")
                                                                    save_csv=False
                                                            else:
                                                                t = t + 2
                                                                print("El decent es un valor Nulo")
                                                    else:
                                                        print("Error no so much to locate Plaintiff")
                                    else:
                                        print("El Pantflit era un JOHN o JANE DOE")

                                else:
                                    p=11
                                    print("El pamflit era una Empresa.")
                                    save_csv=False
                         # Si contien Plaintiff  lo regresamos y añadimos false al save_csv Necesitamos dos back() para regresar
                        if (save_csv):
                            with open(str(choice2)+ "-"+ str(choice) +"-" + str(fecha_inicial) + "--"+ str(fecha2)+'.csv', 'a') as csvFile:
                                data_writer = csv.writer(csvFile)
                                data_writer.writerow([first_name, last_name, addres_petitioner, city_petitioner,
                                      state_petitioner, zip_petitioner
                                    , addres_descendent,city_descendent, state_descendent, zip_descendent, case])
                         # Guardamos  en el CSV los datos
                        else:
                            print("El elemento no se agrego ya que no cumple con los requerimientos para almacenarse.")
                        # Mandamos un mensaje si no se puede guadar como en caso que el Panfit y Defendet sean empresas
                        # No añadimos Ningun back

                        #Fuera del While es que ya salimos de iterar el dato que nos interesaba procedemso a ingresar los back para regresar a la lista de casos a evaluar
                        browser.back()
                        browser.back()



                    else:
                        print("No es el tipo de caso requerido")
                        time.sleep(3)
                        browser.back()
                        time.sleep(3)
                # Si el tipo de caso no es correcto regresamos a la pagina a buscar mas casos
                #Solo se necesitaba un back y ya se agrego

               #Lista general de Casos
               else:
                   print("Uno de Los involucrados era UN LLC o INC")







               #Aumentamos Ya despues de Todas las Validaciones
               i=i+2
            else:
                i=i+2



          print("LLEGANDO A FIN DE LA PAGINA !!!")
          initial_page=initial_page+1
          count_page=count_page+1
          print("LA SIGUIENTE  PAGINA ES : " + str(count_page))


        browser.close()


