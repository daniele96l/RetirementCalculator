import random

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt

#About FIRE moevement https://www.youtube.com/watch?v=SEItn9Csitg&t=736s

#Things to implement
#1) Different asset allocation
#1a) Bond tent
#2) Mostrare anche quanto il mio stipendio (o meglio il mio deposit) sta crescendo
#4) leverage
#5) Barista FIRE, working part time to cover % of your expenses


def Calculator(mortodifame,statistical_y,vector_years, vecotr_FireNumber):

    growth =  readFile() #leggo da un file i dati storici
    year = random.randrange(0, len(growth)) #indice che itirerà sulla lista
    interest_rate = 0.07 #is is uses to calculate the growth of your portfolio
    inflation_rate = 0.03 #this is the inflation rate of the COL
    deposit_raise = 0.03 #increase deposit alongside with inflation
    paycheck_raise = 0.00 #you will not be junior for the rest of your life
    net_gain = 0
    saveMore = True #variable that we are going to use in the code , just to get out of the IF when we got into the FIRE numner
    m_depo = 1000  #yout montly deposit
    m_ex = 2000 #your montly expenses will be uses to calculate your FIRE number + inflation
    money_invested = 0
    starting_age = 25
    years = 25 #your age
    withdrawalrate = 0.04  #safe withdrawal rate, i think that 3.5% is okay if you retire for 50 years
    #https://www.moneyguy.com/2020/11/what-is-the-safe-withdrawal-rate-for-fire/
    fees = 0.002 #usually 0.3%
    fire_number = m_ex*12*(1/withdrawalrate) #this is your fire number based on the n% rule https://www.youtube.com/watch?v=z7rH7h7ljHg

    portfolio_value = 0 #initial portfolio value
    retirement_fund = 0
    vector_portfolio = []

    while(saveMore):
        if(fire_number >= portfolio_value):
           # print(years)
            interest_rate = float(growth[year])/100
            fire_number = fire_number * (1 + inflation_rate) #increase my FIRE number according to iflation
            if(year>= len(growth)-1):  #evito di uscire fuori dal range dei miei dati tornando all'inizio
                year = 0
            portfolio_value = portfolio_value * (1 + interest_rate)   #Increase my portgolio value with the interest rate dato dai dati storici
            portfolio_value = portfolio_value*(1-fees) #brokerage fees
            m_depo = m_depo*(1+deposit_raise+paycheck_raise) #does my deposit (paycheck) increse ovetime?
            money_invested+= m_depo* 12
            portfolio_value += (m_depo * 12) #add my deposit to the portfolio
            #Just create the vectors for the plot
            vector_portfolio.append(portfolio_value)
            statistical_y.append(portfolio_value)
            vector_years.append(years)
            vecotr_FireNumber.append(fire_number)

           # print("Fire Number increased with inflation" + str(int(fire_number)))
            #print("Portfolio " + str(int(portfolio_value))) okr

            years = years + 1
            year += 1

        else:
            saveMore= False
            retirement_fund = portfolio_value

    while ( saveMore==False and years < 80):

        capital_gain_tax = 0.26
        tax_minus = -1+(1)/(1-capital_gain_tax) #formula per calcolare quanti soldi devo prendere in modo da avere un 4% netto esentasse
        net_gain = retirement_fund - money_invested
        percentage_of_gains = net_gain/retirement_fund
        #–--------------------
        x = 1 + percentage_of_gains*tax_minus

        print(x) #circa 1.3
      
        #-------------------- sta roba non funziona, se metto x sotto il failuer rate diventa 0
        if(x<0):
            x= -x
        retirement_fund -= (m_ex*12*(1.3))*pow((1 + inflation_rate), years - starting_age) #1.3 dovrebbe essere i soldi che devo prendere in più per compensare le tasse da capital gain

        #print(m_ex*12 * pow((1 + inflation_rate), years- starting_age))
        if (year >= len(growth) - 1):  # evito di uscire fuori dal range dei miei dati tornando all'inizio
            year = 0
        #retirement_fund = retirement_fund * (1 + 0.07)
        retirement_fund = retirement_fund * (1+float(growth[year])/100)
        retirement_fund = retirement_fund * (1 - fees)  # brokerage fees

        vector_portfolio.append(retirement_fund)  #questo è il valore più importante cazoooooooo
        statistical_y.append(retirement_fund)
        vector_years.append(years)
        vecotr_FireNumber.append(fire_number)
        years += 1
        year += 1

        if(retirement_fund<=0):
            mortodifame += 1
            break



    return mortodifame, statistical_y, vector_years, vecotr_FireNumber


def readFile():
    fileName = "Global.txt"
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def main():
    statistical_y = []
    vector_years = []
    vecotr_FireNumber = []
    mortodifame = 0
    i=0
    n_simulations = 100
    while(i<n_simulations):
        mortodifame,statistical_y,vector_years, vecotr_FireNumber = Calculator(mortodifame,statistical_y,vector_years,vecotr_FireNumber);
        i+=1


    print("-------------")
    print("Failure rate = " + " " + str((mortodifame/n_simulations)*100) + "%")
    print("-------------")

    plt.xlabel('x - Age')
    plt.ylabel('y - NW')
    plt.legend()
    plt.title('FIRE calculator')
    ax = sns.lineplot(vector_years, statistical_y, label="NW", ci = 100)
    ax = sns.lineplot(vector_years, vecotr_FireNumber, label = "FIRE number growth with inflation")


    plt.show()


main()