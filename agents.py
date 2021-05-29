import sys
import os
import math
# from bank_reserves.random_walk import RandomWalker
import pandas as pd
import random, pickle, time
from datetime import datetime
# import json

class Consumer():
    def __init__(self, unique_id):
        # initialize the parent class with required parameters
        # for tracking total value of loans outstanding
        # self.network_capacity=self.random.randint(1,10)
        self.if_update = False
        self.unique_id = unique_id
        self.step_count = 0
        self.mMTC_usage_ratio = round(random.uniform(0,1),1)
        self.URLLC_usage_ratio = 1-self.mMTC_usage_ratio
        self.scale = random.randint(0,10)
        self.URLLC_scale = self.URLLC_usage_ratio*self.scale
        self.mMTC_scale = self.mMTC_usage_ratio*self.scale
        self.mMTC_cost = 1
        self.URLLC_cost = 1.4
        self.cost = self.mMTC_scale*self.mMTC_cost + self.URLLC_scale*self.URLLC_cost
        self.willingness_to_pay = self.cost + round(random.uniform(-2.2,2.2),2)
        self.willingness_to_pay_copy = self.willingness_to_pay

    def mMTC_scale_later(self, step):
        if self.if_update:
            self.mMTC_scale += 0.20*step
    
    def URLLC_scale_later(self, step):
        if self.if_update:
            self.URLLC_scale += 0.12*step
        # print("self.awareness")
    def cost_later(self, step):
        if self.if_update:
            self.cost = self.mMTC_scale*self.mMTC_cost + self.URLLC_scale*self.URLLC_cost

    def update_willingness_to_pay(self, step):
        if self.if_update:    
            self.willingness_to_pay_copy = self.cost - 0.05*step + round(random.uniform(-0.8,4),2)
            # print(self.willingness_to_pay_copy)


class SystemIntegrator():
    def __init__(self, unique_id, consumer_list):
        # initialize the parent class with required parameters
        # super().__init__(unique_id, model)
        # for tracking total value of loans outstanding
        self.unique_id = unique_id   
        self.consumers = consumer_list
        self.hardware_investment = 0 
        self.total_revenue = 0
        self.total_mMTC_services = 0
        self.total_URLLC_services = 0
        self.in_inv_list = []
        # self.network_investment=network_investment
        # self.price = price

    def add_investment(self, step):
        self.total_revenue = 0
        self.total_mMTC_services = 0
        self.total_URLLC_services = 0
        self.number_of_active_consumers=0
        for i in self.consumers:
            
            if i.willingness_to_pay_copy >= i.cost and i.if_update==True:
                self.number_of_active_consumers+=1
                self.total_revenue += i.cost #only positive transaction results should be counted
                self.total_mMTC_services += i.mMTC_scale
                self.total_URLLC_services += i.URLLC_scale
                print("Step: {}, SI_ID: {}, CustID: {}, revenue: {}, mmtc: {}, urllc: {}, mmtc_scale: {}, urllc_scale: {}, cost: {}".format(step, self.unique_id, i.unique_id, self.total_revenue, self.total_mMTC_services, self.total_URLLC_services, i.mMTC_scale, i.URLLC_scale, i.cost))
                # self.in_inv = price*(total_network_density + total_data_services)
            
        self.in_inv_list.append([self.total_revenue, self.total_mMTC_services, self.total_URLLC_services,
                                 self.number_of_active_consumers])
        # print(self.in_inv_list)

    def create_si_df(self):
        self.in_inv_df = pd.DataFrame(data=self.in_inv_list, columns=["total_returns", "total_mMTC_services_SI", "total_URLLC_services_SI", "number_of_active_consumers"])
        self.in_inv_df.to_csv("si_in_inv" + str(self.unique_id) + ".csv")  
#No more attributes, pay everything to the ISPs: Add from all ISPs and pay it forward to their respective ISPs

class ISP():
    def __init__(self, unique_id, system_integrator_list, market_share, investment_URLLC, investment_mMTC, URLLC_spectrum_capacity, mMTC_spectrum_capacity, URLLC_infrastructure_cost, mMTC_infrastructure_cost):
        # initialize the parent class with required parameters
        # super().__init__(unique_id, model)
        # for tracking total value of loans outstanding
        """percent of deposits the bank must keep in reserves - this is a
           UserSettableParameter in server.py"""
        self.unique_id=unique_id
        self.system_integrator=system_integrator_list   
        self.market_share=market_share
        self.URLLC_spectrum_capacity = URLLC_spectrum_capacity
        self.mMTC_spectrum_capacity = mMTC_spectrum_capacity
        self.URLLC_infrastructure_cost = URLLC_infrastructure_cost
        self.mMTC_infrastructure_cost = mMTC_infrastructure_cost
        self.URLLC_total_cost = (self.market_share * ((investment_URLLC)*0.5)) + self.URLLC_infrastructure_cost
        self.mMTC_total_cost = (self.market_share * ((investment_mMTC)*0.5)) + self.mMTC_infrastructure_cost
        self.total_cost = self.URLLC_total_cost + self.mMTC_total_cost
        # self.price_per_unit_service = 20
        self.total_returns=0
        self.total_URLLC_services_ISP=0
        self.total_mMTC_services_ISP=0
        self.total_returns_list=[]
        
    def update_returns(self):
        self.total_returns=0
        self.total_URLLC_services_ISP=0
        self.total_mMTC_services_ISP=0
        for i in self.system_integrator:
            self.total_returns+=(i.total_revenue*0.70)
            self.total_mMTC_services_ISP+=i.total_mMTC_services
            self.total_URLLC_services_ISP+=i.total_URLLC_services
        self.total_returns_list.append([self.total_returns, self.total_mMTC_services_ISP, self.total_URLLC_services_ISP])
        # print(self.total_returns_list)

    def create_isp_df(self):
        self.total_returns_df=pd.DataFrame(data=self.total_returns_list, columns=["total_returns", "total_mMTC_services_ISP", "total_URLLC_services_ISP"])
        self.total_returns_df.to_csv("isp_total_returns"+str(self.unique_id)+".csv")

investment_URLLC=80
investment_mMTC=20

class City():
    def __init__(self, isp_list):
        # initialize the parent class with required parameters
        # super().__init__()
        self.city_investment_URLLC=investment_URLLC*0.5
        self.city_investment_mMTC=investment_mMTC*0.5
        self.total_investment=self.city_investment_mMTC+self.city_investment_URLLC
        self.initial_investment = self.total_investment*0.5
        # self.step_count=0
        # self.area=area
        # self.population=population
        # self.pop_density=self.population/self.area
        self.ISPs=isp_list
        self.total_returns=0
        self.total_URLLC_services_City=0
        self.total_mMTC_services_City=0
        self.total_returns_list=[]
        
    def update_returns(self):
        self.total_returns=0
        self.total_URLLC_services_City=0
        self.total_mMTC_services_City=0
        for i in self.ISPs:
            self.total_returns+=(i.total_returns*0.12)
            self.total_mMTC_services_City+=i.total_mMTC_services_ISP
            self.total_URLLC_services_City+=i.total_URLLC_services_ISP

        self.total_returns_list.append([self.total_returns,self.total_mMTC_services_City, self.total_URLLC_services_City])

    def create_city_df(self):
        self.total_returns_df=pd.DataFrame(data=self.total_returns_list, columns=["total_returns", "total_mMTC_services_City", "total_URLLC_services_City"])
        self.total_returns_df.to_csv("city_total_returns.csv")  

# class TSP():
#     def __init__(self, unique_id, model, price=50):
#         # initialize the parent class with required parameters
#         super().__init__(unique_id, model)
#         # for tracking total value of loans outstanding
#         """percent of deposits the bank must keep in reserves - this is a
#            UserSettableParameter in server.py"""
#         self.price = price

# class Regulator():
#     def __init__(self, unique_id, model, initial_investment, people, price=50, budget=1000):
#         # initialize the parent class with required parameters
#         super().__init__(unique_id, model)
#         # for tracking total value of loans outstanding
#         # self.bank_loans = 0
#         self.data_collected = 0
#         self.budget=budget
#         self.initial_investment = 200
#         self.price=price
#         self.step_count=0
#         self.cost_eff=0
#         self.people=people
#         self.number_of_locations = self.initial_investment/self.price
#         self.location_list = []
#         self.cost_eff_list =[]
#         """percent of deposits the bank must keep in reserves - this is a
#            UserSettableParameter in server.py"""
#         self.total_awareness = 0
#         # for tracking total value of deposits
#     def cost_effectiveness(self, price) :
#         citizen_awareness=0
#         for i in self.people:
#             citizen_awareness+=i.awareness
#         self.cost_eff = price*self.number_of_locations/(citizen_awareness)
#         self.cost_eff_list.append(self.cost_eff)
#         self.cost_eff_df=pd.DataFrame(self.cost_eff_list)
#         self.cost_eff_df.to_csv("costeff.csv")
#     def number_of_locations_later(self, cost_eff_threshold):
#         if self.cost_eff > cost_eff_threshold:
#             if (self.number_of_locations+1)*self.price< self.budget:
#                 self.number_of_locations +=1
#         self.location_list.append(self.number_of_locations)
#         self.num_loc_df=pd.DataFrame(self.location_list)
#         self.num_loc_df.to_csv("num_loc.csv")
#         # self.num_loc_df=self.num_loc_df.append(location_list, ignore_index=True)
#     def data_collected_later(self):        
#         self.data_collected=self.number_of_locations*self.step_count
# # subclass of RandomWalker, which is subclass to Mesa 
#     def step(self):
#         self.step_count+=1
#         for i in self.people:
#             i.step1(self.data_collected, self.step_count)
#         self.cost_effectiveness( self.price)
#         self.number_of_locations_later( 1)
#         self.data_collected_later()
#         # print("self.awareness")

# class Person(RandomWalker):
#     def __init__(self, unique_id, pos, model, moore, tsp, awareness_threshold):
#         # init parent class with required parameters
#         super().__init__(unique_id, pos, model, moore=moore)
#         # the amount of awareness
#         self.awareness_threshold=awareness_threshold
#         self.awareness = self.random.randint(1, self.awareness_threshold + 1)
#         self.awareness_copy = self.awareness
#         self.tsp=tsp
#         # self.regulator=regulator
#         """start everyone off with a random amount in their wallet from 1 to a
#            user settable rich threshold amount"""
#     def step(self):
#         self.random_move()
#        # step is called for each agent in model.BankReservesModel.schedule.step()
#     def step1(self,data_collected, step_count):
#         # move to a cell in my Moore neighborhood
#         # self.random_move()
#         self.awareness_later(data_collected, step_count)
#         # print(self.awareness)
#         # trade
#     def awareness_later(self,data_collected,step_count):
#         if self.awareness<1.35*self.awareness_copy:
#             self.awareness=math.sqrt(4*(0.01)*data_collected) + self.awareness_copy
#         else:
#             self.awareness=-2*math.sqrt(0.002*data_collected) + self.awareness_copy

#             # y=-2\left(0.005x\right)^{\frac{1}{2}}+2
#     def pollution_later(self,data_collected,step_count):
#         self.pollution=math.sqrt(4*(0.02)*data_collected + self.awareness_copy)