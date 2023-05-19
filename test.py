from matplotlib import pyplot as plt
import random as r
class humidity_sensor:
    def __init__(self):
        self.days = 0
        self.humidity = 0
        def generate_soil_humidity_function():

            # Generate data for x-axis (time)
            days = [x for x in range(30)]
            
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
    
    def plot_line(self):
        plt.plot(self.days, self.humidity)
        plt.xlabel('Time')
        plt.ylabel('Soil Humidity')
        plt.title('Soil Humidity Function')
        plt.ylim(-10, 110)  # Set y-axis limits to accommodate values below 0 and above 100
        plt.grid(True)
        plt.show()

a = humidity_sensor()

a.plot_line()