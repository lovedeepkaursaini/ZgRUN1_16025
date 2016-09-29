#!usr/bin/python
import sys, math
import ROOT
from ROOT import TFile, TH1F, TF1, TCanvas, TLegend, TGraphErrors, gROOT, gPad
from array import array
import CMS_lumi, tdrstyle

#set the tdr style
tdrstyle.setTDRStyle()


#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_8TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "8 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod =2

#gStyle.SetPadRightMargin(0.06)
#gStyle.SetPadTopMargin(0.06)

mass = [750,1000,1500,2000,2500,3000,3500]
ABeffi = [0.0930282,0.159127,0.179342,0.183382, 0.175388, 0.152587, 0.113807, 0.0720345]
coreABeffi = [0.0908885, 0.157378, 0.177555, 0.181948, 0.173438, 0.148577, 0.101968, 0.0407794]
Beffi = [0.0124, 0.023384, 0.0274036, 0.028549, 0.0258209, 0.0248353, 0.0204728, 0.0147145]
coreBeffi = [0.0123314, 0.0233232, 0.0273066, 0.0283336, 0.0255426, 0.0239058, 0.0204875, 0.0147145]
#xsection = [3.39, 3.77, 4.22, 4.27, 3.82, 2.87, 1.83]

y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
x = []
ey = []
ex = []

xs=1
for im in mass:
  inf = TFile.Open('histos_signal-'+str(im)+'.root')

  print inf
  h1 = inf.Get('hCounterWtb')#sr
  h2 = inf.Get('hCounterWtb')#sr
  h3 = inf.Get('hCounterWtb')#sr
  N1 = h1.GetBinContent(17)
  N2 = h2.GetBinContent(18)
  N3 = h3.GetBinContent(19)
  p1 = N1 #(GenEvt[xs]*19.7*1000*0.1)
  p2 = N2 #Beffi[xs]#N2
  p3 = N3#ABeffi[xs]#N3
  pdiffdn = math.fabs(p2-p1)/p2
  pdiffup = math.fabs(p3-p2)/p2

 # print str(im), ' & ', int(round(p1*100,0)), '$\\%$ & ', int(round(p2*100,0)) , '$\\%$  & ', int(round(p3*100,0)) ,'$\\%$ \\\\'
  y1.append(p1)
  y2.append(p2)
  y3.append(p3)
  y4.append(pdiffdn)
  y5.append(pdiffup)
  x.append(im)
  ey.append(0.0)
  ex.append(0.0)
  print str(im), p1, p2, p3
  xs=xs+1

vy1 = array('d',y1)
vy2 = array('d',y2)
vy3 = array('d',y3)
vy4 = array('d',y4)
vy5 = array('d',y5)
vx = array('d',x)
vey = array('d',ey)
vex = array('d',ex)

g1 = TGraphErrors(len(vx),vx,vy1,vex,vey)
g2 = TGraphErrors(len(vx),vx,vy2,vex,vey)
g3 = TGraphErrors(len(vx),vx,vy3,vex,vey)
gDiffd = TGraphErrors(len(vx),vx,vy4,vex,vey)
gDiffu = TGraphErrors(len(vx),vx,vy5,vex,vey)

g1.SetLineColor(ROOT.kBlue)
g2.SetLineColor(ROOT.kRed)
g3.SetLineColor(ROOT.kBlack)
g1.SetMarkerColor(ROOT.kBlue)
g2.SetMarkerColor(ROOT.kRed)
g3.SetMarkerColor(ROOT.kBlack)
g1.SetMarkerStyle(20)
g2.SetMarkerStyle(21)
g3.SetMarkerStyle(23)
g1.SetLineWidth(2)
g2.SetLineWidth(2)
g3.SetLineWidth(2)

can = TCanvas('SignalEfficiency','SignalEfficiency',600,600)
#can.SetGrid()
can.SetLogy();
g3.GetXaxis().SetNdivisions(505)
g3.GetXaxis().SetTitle('Resonance Mass [GeV]')
g3.GetYaxis().SetTitle('A#times#epsilon')
g3.GetYaxis().SetNdivisions(505)
g2.GetYaxis().SetNdivisions(505)
g3.GetXaxis().SetRangeUser(650,2500)
g3.GetYaxis().SetRangeUser(0.0001,1)
#g1.Fit("pol3");
f4 = TF1("f4","pol3",0,10000)
f4.SetLineWidth(2)
f4.SetLineColor(ROOT.kBlack);
f3 = TF1("f3","pol3",0,10000)
f3.SetLineWidth(2)
f3.SetLineColor(ROOT.kRed);
g2.Fit("f3")
g3.Fit("f4")
print f4.GetParameter(1), f4.Eval(750)
g1.SetLineColor(ROOT.kBlue)
g2.SetLineColor(ROOT.kRed)
g3.SetLineColor(ROOT.kBlack)
#g1.Draw('text,APE')
g3.Draw('text,APE')
g2.Draw('samePE')

leg = TLegend(0.2,0.25,0.5,0.4,"#frac{#Gamma}{m}=0.014%")
#leg.AddEntry(g1,'Z-tagging','LP')
leg.AddEntry(g3,'anti-b-tag category','LP')
leg.AddEntry(g2,'b-tag category','LP')
#leg.AddEntry(g1,'JER-Down','LP')
#leg.AddEntry(g2,'Central','LP')
#leg.AddEntry(g3,'JER-Up','LP')
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.04)
leg.Draw()

CMS_lumi.CMS_lumi(can, iPeriod, iPos)
can.cd()
can.Update()

#----- keep the GUI alive ------------
if __name__ == '__main__':
  rep = ''
  while not rep in ['q','Q']:
    rep = raw_input('enter "q" to quit: ')
    if 1 < len(rep):
      rep = rep[0]


