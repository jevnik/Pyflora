import random
import math
import numpy as np
import random as r
import matplotlib.pyplot as plt

class sunlight_sensor:
    def __init__(self):
        self.days = 0
        self.sunlight = 0
        def generate_soil_sunlight_function():
            # Generate data for x-axis (time)
            days = [(-1)*x for x in range(30)]
            
            # Generate data for y-axis (soil sunlight) with randomness
            sunlight = []
            a = r.randint(0,5000)
            for i in range(len(days)):
                a = a + r.choice((-1,1))*r.randint(0,100)
                if a < 0:
                    a = 0
                sunlight.append(a)
            return days, sunlight
        
        self.days = generate_soil_sunlight_function()[0]
        self.sunlight = generate_soil_sunlight_function()[1]

    
    def plot_line(self,req):
        req = [req for x in range(30)]
        plt.plot(self.days,req,label="Required")
        plt.plot(self.days, self.sunlight,label="Measured sunlight")
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('sunlight')
        plt.title('sunlight Function')
        plt.grid(True)
        plt.show()

class humidity_sensor:
    def __init__(self):
        self.days = 0
        self.humidity = 0
        def generate_soil_humidity_function():

            # Generate data for x-axis (time)
            days = [x*(-1) for x in range(30)]
            # Generate data for y-axis (soil humidity) with randomness
            humidity = []
            a = r.randint(25,75)
            for i in range(len(days)):
                a = a + -1*r.randint(0,10)
                if a > 100:
                    a = 100
                elif a < 0:
                    a = 0
                
                if i % 5 == 0:
                    a += 40

                if a > 100:
                    a = 100
                humidity.append(a)
            return days, humidity
        
        self.days = generate_soil_humidity_function()[0]
        self.humidity = generate_soil_humidity_function()[1]
    
    def plot_line(self,req):
        req = [req for x in range(30)]
        plt.plot(self.days,req,label="Required")
        plt.plot(self.days, self.humidity,label="Measured humidity")
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Soil Humidity')
        plt.title('Soil Humidity Function')
        plt.ylim(-10, 110)  # Set y-axis limits to accommodate values below 0 and above 100
        plt.grid(True)
        plt.show()

class salinity_sensor:
    def __init__(self):
        self.days = 0
        self.salinity = 0
        def generate_soil_salinity_function():
            # Generate data for x-axis (time)
            days = [(-1)*x for x in range(30)]
            
            # Generate data for y-axis (soil salinity) with randomness
            salinity = []
            a = r.random()/10
            for i in range(len(days)):
                a = a + r.choice((-1,1))*r.random()/100
                if a < 0:
                    a = 0
                elif a > 1:
                    a = 1
                salinity.append(a)
            return days, salinity
        
        self.days = generate_soil_salinity_function()[0]
        self.salinity = generate_soil_salinity_function()[1]
    
    def plot_line(self,req):
        req = [req for x in range(30)]
        plt.plot(self.days,req,label="Required")
        plt.plot(self.days, self.salinity,label="Measured slainity")
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('salinity')
        plt.title('salinity Function')
        plt.grid(True)
        plt.show()

class ph_sensor:
    def __init__(self):
        self.ph = random.randint(3,9)
        self.days = [(-1)*x for x in range(30)]
        self.ph = [self.ph for x in range(30)]

    def plot_line(self):
        plt.plot(self.days, self.ph)
        plt.xlabel('Time')
        plt.ylabel('sunlight')
        plt.title('sunlight Function')
        plt.grid(True)
        plt.show()


