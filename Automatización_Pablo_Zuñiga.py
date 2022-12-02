import netmiko
import re


SW1= {
        "device_type":"cisco_ios",
        "host":"192.168.0.1",
        "username":"cisco",
        "password":'cisco',
        "port":"22",
        "secret":"cisco",
        }

CONEX= netmiko.ConnectHandler(**SW1)
print("CONEXION ESTABLECIDA")
print("------"*18)

x = input("introduce la mac address en el siguiente formato xxxx.xxxx.xxxx.xxxx: ")
    #f076.1cce.5da9
while True:

    COMANDO = CONEX.send_command("sh mac address-table")
    #print(COMANDO)
    print("----------"*18)


    f = re.search(x, COMANDO)
    print("---------"*18)


    if f is not None:
        
        h = "show mac address-table address"+" "+x
        q = CONEX.send_command(h)
        #print(q)
        print("---------"*18)

        PORT = re.findall(r"\w\w\w?\d\/\d\/?\d?\d?", q)
        PUERTO= (PORT[0])

        print("---------"*18)
        
        print("MAC address encontrada en el puerto: ", PUERTO)

        cdp  = CONEX.send_command("sh cdp neigh")
        
        PORT2 = re.findall(r"(Gi|Fa)", cdp)#((Gi|Fa)|\d\/\d\/?\d?\d?)
        PORT3 = re.findall(r"(\d\/\d\/?\d?\d?)", cdp)
        
    
        try:
       

            for w in range (0,20,2):
                PRT=(PORT2[w])
                PRT2=(PORT3[w])
                PRT3= (PRT)+(PRT2)


                if PRT3 == PUERTO:
                    
                    break
                
        except IndexError:
            
            print("Busqueda finalizada!")
            
            break
            



        PRT=(PORT2[w])
        PRT2=(PORT3[w])
        PRT3= (PRT)+(PRT2)
        

        posID=w//2
        posIP=w*2//2

        

        if PRT3 == PUERTO:


            
            Ndet = CONEX.send_command("sh cdp neigh det")
            LaIP= re.findall(r"\d\d\d[.]\d\d?\d?[.]\d\d?\d?[.]\d\d?\d?", Ndet)
            ID= re.findall(r"Device.ID: ..?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?.?", Ndet)
            SWITCH = (ID[posID])
            IP =(LaIP[posIP])
            


            
            SW2= {
                    "device_type":"cisco_ios",
                    "host":IP,
                    "username":"cisco",
                    "password":'cisco',
                    "port":"22",
                    "secret":"cisco",
                 }


            
                
            CONEX= netmiko.ConnectHandler(**SW2)
            print("CONECTADO A: ", SWITCH)

            Hdet = CONEX.send_command("sh running-config | include hos")
            HOST= re.findall(r"[^hostname ]..?.?.?.?.?.?.?.?.?", Hdet)
            fd= (HOST[0])
            print("ACTUAL: ", fd)
            
        

        

    else:
        print("Esa mac address no se encuentra en la tabla!")

        break


