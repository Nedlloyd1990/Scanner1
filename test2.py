import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date
import datetime as dt
import pandas_ta as ta
import datetime
import talib




# date1=datetime.datetime(2021,12,30)


list1=["ZEEL.NS","YESBANK.NS","WIPRO.NS","WHIRLPOOL.NS","VOLTAS.NS","IDEA.NS","VEDL.NS","VBL.NS",
"MCDOWELL-N.NS","UBL.NS","UNIONBANK.NS","ULTRACEMCO.NS","UPL.NS","TRENT.NS","TORNTPOWER.NS","TORNTPHARM.NS",
"TITAN.NS","RAMCOCEM.NS","TECHM.NS","TATASTEEL.NS","TATAPOWER.NS","TATAMOTORS.NS","TATAELXSI.NS",
"TATACONSUM.NS","TCS.NS","TATACOMM.NS","TATACHEM.NS","TVSMOTOR.NS","SYNGENE.NS","SUNTV.NS","SUNPHARMA.NS",
"SAIL.NS","SBIN.NS","SONACOMS.NS","SIEMENS.NS","SRTRANSFIN.NS","SHREECEM.NS","SANOFI.NS","SRF.NS","SBILIFE.NS",
"SBICARD.NS","RELIANCE.NS","RECLTD.NS","RBLBANK.NS","PNB.NS","PGHH.NS","PRESTIGE.NS","POWERGRID.NS","PFC.NS",
"POLYCAB.NS","PEL.NS","PIDILITIND.NS","PFIZER.NS","PETRONET.NS","PAGEIND.NS","PIIND.NS","OIL.NS","ONGC.NS",
"OBEROIRLTY.NS","NAM-INDIA.NS","NESTLEIND.NS","NAVINFLUOR.NS","NATIONALUM.NS","NTPC.NS","NMDC.NS","NATCOPHARM.NS",
"MUTHOOTFIN.NS","MPHASIS.NS","MINDTREE.NS","MFSL.NS","MARUTI.NS","MARICO.NS","MANAPPURAM.NS","M&M.NS","M&MFIN.NS",
"MGL.NS","MRF.NS","LUPIN.NS","LAURUSLABS.NS","LT.NS","LTI.NS","LICHSGFIN.NS","LTTS.NS","L&TFH.NS","KOTAKBANK.NS",
"JUBLFOOD.NS","JINDALSTEL.NS","JSWSTEEL.NS","JSWENERGY.NS","IPCALAB.NS","INDIGO.NS","INFY.NS","NAUKRI.NS",
"INDUSINDBK.NS","INDUSTOWER.NS","IGL.NS","IRFC.NS","IRCTC.NS","IOC.NS","INDHOTEL.NS","INDIANB.NS","INDIAMART.NS",
"ITC.NS","IDFCFIRSTB.NS","ISEC.NS","ICICIPRULI.NS","ICICIGI.NS","ICICIBANK.NS","HDFC.NS","HINDZINC.NS",
"HINDUNILVR.NS","HINDPETRO.NS","HINDCOPPER.NS","HAL.NS","HINDALCO.NS","HEROMOTOCO.NS","HAVELLS.NS","HDFCLIFE.NS",
"HDFCBANK.NS","HDFCAMC.NS","HCLTECH.NS","GSPL.NS","GUJGASLTD.NS","GRASIM.NS","GODREJPROP.NS","GODREJIND.NS",
"GODREJCP.NS","GLENMARK.NS","GLAND.NS","GAIL.NS","FORTIS.NS","FEDERALBNK.NS","EXIDEIND.NS","ESCORTS.NS",
"ENDURANCE.NS","EMAMILTD.NS","EICHERMOT.NS","DRREDDY.NS","LALPATHLAB.NS","DIXON.NS","DIVISLAB.NS","DHANI.NS",
"DEEPAKNTR.NS","DALBHARAT.NS","DABUR.NS","DLF.NS","CUMMINSIND.NS","CROMPTON.NS","COROMANDEL.NS","CONCOR.NS",
"COLPAL.NS","COFORGE.NS","COALINDIA.NS","CUB.NS","CIPLA.NS","CHOLAFIN.NS","CASTROLIND.NS","CANBK.NS","CADILAHC.NS",
"BRITANNIA.NS","BOSCHLTD.NS","BIOCON.NS","BHARTIARTL.NS","BPCL.NS","BHEL.NS","BHARATFORG.NS","BEL.NS","BERGEPAINT.NS",
"BATAINDIA.NS","BANKINDIA.NS","BANKBARODA.NS","BANDHANBNK.NS","BALKRISIND.NS","BAJAJHLDNG.NS","BAJAJFINSV.NS",
"BAJFINANCE.NS","BAJAJ-AUTO.NS","AXISBANK.NS","DMART.NS","AUROPHARMA.NS","ASTRAL.NS","ASIANPAINT.NS","ASHOKLEY.NS",
"APOLLOTYRE.NS","APOLLOHOSP.NS","AMBUJACEM.NS","AMARAJABAT.NS","ALKEM.NS","APLLTD.NS","AJANTPHARM.NS","ABFRL.NS",
"ABCAPITAL.NS","ADANITRANS.NS","ATGL.NS","ADANIPORTS.NS","ADANIGREEN.NS","ADANIENT.NS","AARTIIND.NS","AUBANK.NS","ACC.NS",]

script_name=[]
prev_srsi=[]
curr_srsi=[]
ma=[]
lastp=[]
MAsignal=[]



st.write("""
# Stochastic RSI Scanner
Datasource is yfinance and calculation done using ta-lib
""")

date1=st.sidebar.date_input("enterdate",dt.date.today())


values=["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
default_ix = values.index("1d")
timeInterval=st.sidebar.selectbox('Time Frame',(values),default_ix)


for stkname in list1:
	data= yf.Ticker(stkname)

	data_historical = data.history(start=date1-dt.timedelta(100), end=date1, interval=timeInterval)
	data_historical['rsi']=talib.RSI(data_historical['Close'],14)
	# data_historical['fastk'],data_historical['fastd']=talib.STOCHRSI(data_historical['Close'], 14, 3, 3, 0)
	script_name.append(str(stkname))

	movingAVG=sum(data_historical['Close'][-50:])/50
	ma.append(movingAVG)
	lastp.append(data_historical['Close'][-1])
	MAsignal.append(data_historical['Close'][-1]>movingAVG)

	prevDay_srsi=data_historical['rsi'][-15:-1]
	prev_maxRSI=max(prevDay_srsi)
	prev_minRSI=min(prevDay_srsi)
	prev_srsi1= (((data_historical['rsi'][-2]-prev_minRSI)/(prev_maxRSI-prev_minRSI)))*100
	prev_srsi.append(prev_srsi1)


	currDay_srsi=data_historical['rsi'][-14:]
	curr_maxRSI=max(currDay_srsi)
	curr_minRSI=min(currDay_srsi)
	curr_srsi1= (((data_historical['rsi'][-1]-curr_minRSI)/(curr_maxRSI-curr_minRSI)))*100
	curr_srsi.append(curr_srsi1)
	print(len(script_name))


		

dff=pd.DataFrame({"Script Name":script_name, "Prev_SRSI":prev_srsi, "Current_SRSI":curr_srsi,"Last Price":lastp, "MovingAVG":ma, "MASignal":MAsignal})
st.table(dff[((dff.Prev_SRSI<20) & (dff.Current_SRSI>20)) | ((dff.Prev_SRSI>80) & (dff.Current_SRSI<80)) ])

