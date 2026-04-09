void plot_separation(const char* fileName) {
    TFile *f = TFile::Open(fileName);
    if (!f || f->IsZombie()) {
        printf("Error: Could not open file %s\n", fileName);
        return;
    }

    TCanvas *c1 = new TCanvas("c1", "Figure 1 Replication", 1200, 600);
    c1->Divide(2,1);
    gStyle->SetOptStat(0);
    gStyle->SetPalette(kBird);

    c1->cd(1);
    TH2F *h_gen = (TH2F*)f->Get("demo/h_GenSep_Crystals");
    if(h_gen) {
        h_gen->SetTitle("GEN Opening Angle ; |#Delta i#eta|; |#Delta i#phi|");
        h_gen->GetXaxis()->SetRangeUser(0, 30);
        h_gen->GetYaxis()->SetRangeUser(0, 30);
        h_gen->SetMarkerStyle(20);
        h_gen->SetMarkerSize(1.5);
        h_gen->Draw("COLZ");
    }

    c1->cd(2);
    TH2F *h_eb_center = (TH2F*)f->Get("demo/Hits_EB_Centered");
    if(h_eb_center) {
        h_eb_center->SetTitle("Centered ECAL Energy Pattern; Relative i#eta; Relative i#phi");
        h_eb_center->GetZaxis()->SetTitle("Energy (GeV)");
        h_eb_center->GetZaxis()->SetTitleOffset(1.2);
        h_eb_center->Draw("COLZ");
        //gPad->SetLogz();
        gPad->SetRightMargin(0.15);
    }
    
    c1->SaveAs("CMS_EGM_Figure1_Replication.png");
    /*
    TCanvas *c2 = new TCanvas("c2", "Separation Variables", 1200, 400);
    c2->Divide(3,1);
    gStyle->SetOptStat(1111);

    c2->cd(1);
    TH1F *h_dr = (TH1F*)f->Get("demo/Hits_dR");
    if(h_dr) { 
        h_dr->SetLineColor(kBlue); 
        h_dr->SetLineWidth(2);
        h_dr->Draw(); 
    }

    c2->cd(2);
    TH1F *h_eta = (TH1F*)f->Get("demo/Hits_delta_eta");
    if(h_eta) { 
        h_eta->SetLineColor(kRed); 
        h_eta->SetLineWidth(2);
        h_eta->Draw(); 
    }

    c2->cd(3);
    TH1F *h_phi = (TH1F*)f->Get("demo/Hits_delta_phi");
    if(h_phi) { 
        h_phi->SetLineColor(kGreen+2); 
        h_phi->SetLineWidth(2);
        h_phi->Draw(); 
    }
    
    // c2->SaveAs("Separation_Variables_1D.png");
    */
}
