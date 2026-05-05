import ROOT
from DataFormats.FWLite import Events, Handle

# File path
file_path = 'file:DP1_folder/AToGG_GEN_E10_new_RECO.root'
events = Events(file_path)

# Handle for Rho
rho_handle = Handle('double')
rho_label = ("fixedGridRhoFastjetAll")

# Create a ROOT Histogram
# Parameters: Name, Title, Bins, Min, Max
hist_rho = ROOT.TH1F("hist_rho", "Energy Density (#rho) Distribution; #rho (GeV); Events", 50, 0, 50)

print 'Analyzing events...'
for i, event in enumerate(events):
    try:
        event.getByLabel(rho_label, rho_handle)
        rho_value = rho_handle.product()[0]
        hist_rho.Fill(rho_value)
    except:
        pass
    
    if i % 100 == 0 and i > 0:
        print 'Processed {} events'.format(i)

# --- Plotting Part ---
canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
ROOT.gStyle.SetOptStat(1111) # Show Mean, RMS, etc.
hist_rho.SetLineColor(ROOT.kBlue)
hist_rho.SetLineWidth(2)
hist_rho.Draw()

# Save the plot as a PNG
canvas.SaveAs("rho_distribution.png")
print 'Analysis complete. Plot saved as rho_distribution.png'
