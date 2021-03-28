#!/usr/bin/env python
# coding: utf-8

# In[1]:



class City:
    def __init__(self):
        self.Evs = {
            'C1' : {
                'source' : 'MB',
                'destination': 'LBS',
                'init_battery' : 4,
                'charging' : 3,
                'discharging' : 5,
                'max' : 200,
                'speed' : 24
            },
            "C2": {
                "source": "LLR",
                "destination": "SNIG",
                "init_battery": 15,
                "charging": 8,
                "discharging": 9,
                "max": 100,
                "speed": 25
            },
            "C3": {
                "source": "PAN",
                "destination": "CCD",
                "init_battery": 6,
                "charging": 2,
                "discharging": 3,
                "max": 160,
                "speed": 30
            },
            "C4": {
                "source": "BCRH",
                "destination": "RP",
                "init_battery": 8,
                "charging": 4,
                "discharging": 6,
                "max": 120,
                "speed": 22
            },
            "C5": {
                "source": "MT",
                "destination": "TSG",
                "init_battery": 10,
                "charging": 1,
                "discharging": 2,
                "max": 150,
                "speed": 26
            }
        }
        
        # KGP MAP
        self.graph = {
            'RP' : {
                'MB' : 100,      # MB stands for Main Building
                'LLR' : 400
            },
            "LLR": {
                "LBS": 200,
                "CCD": 150,
                "TSG": 250,
                "RP" : 400
            },
            "LBS": {
                "LLR": 200,
                "PAN": 100
            },
            "PAN": {
                "LBS": 100,
                "BCRH": 200
            },
            "BCRH": {
                "PAN": 200,
                "TSG": 300,
                "SNIG": 650
            },
            "SNIG": {
                "TSG": 350,
                "BCRH": 650,
                "MT": 250
            },
            "MT": {
                "SNIG": 250,
                "MB": 500
            },
            "MB": {
                "RP": 100,
                "MT": 500,
                "CCD": 200
            },
            "CCD": {
                "MB": 200,
                "LLR": 150,
                "TSG": 300
            },
            "TSG": {
                "LLR": 250,
                "BCRH": 300,
                "SNIG": 350
            }
        }
        self.cars = self.Evs.keys()
        self.cities = self.graph.keys()

    def getDistanceBetween(self, cityA, cityB):
        return self.graph[cityA][cityB]
    
    def adjacentCities(self, city):
        return self.graph[city].keys()

    def diksaktra(self):
        global large
        for car in self.cars:
            Ev = self.Evs[car]
            max_dist = Ev['max']*Ev['discharging']
            
            #starting dijkastra
            distances={}
            parents={}
            iterate=[] 
            for city in self.cities:
                distances[city]=large
                if(city!=Ev["source"]):
                    iterate.append(city)
            distances[Ev["source"]]=0
            parents[Ev["source"]]=None
            
            n_cities = self.adjacentCities(Ev["source"])
            for n_city in n_cities:
                parents[n_city]=Ev["source"]
                distances[n_city]=self.getDistanceBetween(Ev["source"],n_city)
            while (len(iterate)):
                min=large
                mincity=None
                for city in iterate:
                    dist= distances[city]
                    if(dist<min):
                        min=dist
                        mincity=city
                iterate.remove(mincity)
                n_cities=self.adjacentCities(mincity)
                for n_city in n_cities:
                    if (self.getDistanceBetween(mincity, n_city)>min):
                        pass 
                    upd=min+self.getDistanceBetween(mincity,n_city)
                    if (upd < distances[n_city]):
                        distances[n_city]=upd
                        parents[n_city]=mincity
            pathlist = []            
            chain=Ev['destination']
            
            #joining chain with parents
            
            while(chain!= None):
                        pathlist.append(chain)
                        chain = parents[chain]
            pathlist1 = pathlist[::-1]
            print(pathlist1)
            
            #Calculating Time to reach destination
            
            time=0
            time=time+ (distances[Ev['destination']]/Ev['speed']) 
            req_battery= (distances[Ev['destination']]/Ev['discharging']) - Ev['init_battery']
            if(req_battery>0):
                time = time + req_battery/Ev['charging']
            print(time)

large = 1000000
Kgp = City()
Kgp.diksaktra()





# In[ ]:




