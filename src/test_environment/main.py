from collectData import CollectData
from regression import Regression
from plot import Plot

def main():
     data = CollectData('192.168.1.69', 'AC:75:1D:57:8A:D8')
     regression = Regression()
     value = input('Would you like to collect data? [y/n] ')
     n = 0
     while(value == 'y' and n<6):
          # collect data foreach distance
          val = data.collect()

          # call AddRSSI of regression
          regression.addRSSI(val) 
          
          print(regression._RSSIAritmetica)
          print(regression._RSSIQuadratica)
          value = input('Would you like to collect data?[y/n] ').strip('\r').strip('\n')
          n += 1
     
     # call regression
     result = regression.linearRegression() 
     print(result)

     # plot line above point with data gave from regression
     p1 = Plot('DEVICE', '-log10(distance)', 'RSSI') 
     p1.pointsAndLine(regression.getLog10Distance(), regression.getRSSIAritmetica(), -1, 1, 100, result['arithmeticK'], result['arithmeticA'])

if __name__=="__main__":
    main()
