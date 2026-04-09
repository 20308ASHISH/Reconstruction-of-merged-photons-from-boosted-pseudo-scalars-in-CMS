#include <memory>
#include <iostream>
#include <fstream>
#include <cmath>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"
#include "SimDataFormats/CaloHit/interface/PCaloHit.h"
#include "SimDataFormats/CaloHit/interface/PCaloHitContainer.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2F.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

class ECAL_Simhits_Analyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit ECAL_Simhits_Analyzer(const edm::ParameterSet&);
  ~ECAL_Simhits_Analyzer() {}

private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override {}

  TH1F* NHits_EB;
  TH2F* Hits_EB;
  TH1F* Hits_dR;
  TH1F* Hits_delta_eta;
  TH1F* Hits_delta_phi;
  TH2F* h_GenSep_Crystals;
  TH2F* Hits_EB_Centered;

  edm::EDGetTokenT<edm::View<reco::GenParticle>> particleToken;
  edm::EDGetTokenT<edm::PCaloHitContainer> pCaloHits_EB_Token;
};

ECAL_Simhits_Analyzer::ECAL_Simhits_Analyzer(const edm::ParameterSet& iConfig){
  usesResource("TFileService");
  particleToken = consumes<edm::View<reco::GenParticle>>(edm::InputTag("genParticles"));
  pCaloHits_EB_Token = consumes<edm::PCaloHitContainer>(edm::InputTag("g4SimHits", "EcalHitsEB", "SIM"));
}

void ECAL_Simhits_Analyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  using namespace std;
  using namespace reco;

  Handle<View<GenParticle>> particle;
  iEvent.getByToken(particleToken, particle);

  int photonCount = 0;
  const GenParticle* g1 = nullptr;
  const GenParticle* g2 = nullptr;

  for (const auto &p : *particle){
    if (p.status() == 1 && p.pdgId() == 22) {
      photonCount++;
      if (photonCount == 1) g1 = &p;
      if (photonCount == 2) g2 = &p;
    }
  }

  if (photonCount < 2) return; 

  double deta = g1->eta() - g2->eta();
  double dphi = reco::deltaPhi(g1->phi(), g2->phi());
  h_GenSep_Crystals->Fill(abs(deta/0.0174), abs(dphi/0.0174));
  
  Hits_delta_phi->Fill(dphi);
  Hits_delta_eta->Fill(deta);
  Hits_dR->Fill(reco::deltaR(g1->eta(), g1->phi(), g2->eta(), g2->phi()));

  Handle<PCaloHitContainer> pCaloHits_EB_Handle;
  iEvent.getByToken(pCaloHits_EB_Token, pCaloHits_EB_Handle);

  ESHandle<CaloGeometry> pG;
  iSetup.get<CaloGeometryRecord>().get(pG);
  const CaloGeometry* geo = pG.product();

  double mid_eta = (g1->eta() + g2->eta()) / 2.0;
  double mid_phi = (g1->phi() + g2->phi()) / 2.0;

  double theta = 2.0 * atan(exp(-mid_eta));
  double r_eb = 129.0; 
  GlobalPoint midPoint(r_eb * cos(mid_phi), r_eb * sin(mid_phi), r_eb / tan(theta));

  const CaloSubdetectorGeometry* barrelGeom = geo->getSubdetectorGeometry(DetId::Ecal, EcalBarrel);
  DetId midId = barrelGeom->getClosestCell(midPoint);
  
  if (midId.det() == DetId::Ecal && midId.subdetId() == EcalBarrel) {
    EBDetId midEB(midId);
    int mid_ieta = midEB.ieta();
    int mid_iphi = midEB.iphi();

    int nHitsInEvent = 0;
    for(auto const& hit : *pCaloHits_EB_Handle){
      EBDetId id(hit.id());
      nHitsInEvent++;
      
      Hits_EB->Fill(id.ieta(), id.iphi(), hit.energy());

      int rel_ieta = (id.ieta() - mid_ieta) + 16;
      int rel_iphi = (id.iphi() - mid_iphi) + 16;
      
      if (id.ieta() * mid_ieta < 0) {
          if (id.ieta() > 0) rel_ieta -= 1;
          else rel_ieta += 1;
      }

      if (rel_ieta >= 0 && rel_ieta < 32 && rel_iphi >= 0 && rel_iphi < 32) {
        Hits_EB_Centered->Fill(rel_ieta, rel_iphi, hit.energy());
      }
    }
    NHits_EB->Fill(nHitsInEvent);
  }
}

void ECAL_Simhits_Analyzer::beginJob() {
  edm::Service<TFileService> fs;
  NHits_EB = fs->make<TH1F>("NHits_EB","Total Hits in EB",500,0, 500);
  Hits_EB = fs->make<TH2F>("Hits_EB","Global Map", 171, -85.5, 85.5, 360, 0.5, 360.5);
  Hits_dR = fs->make<TH1F>("Hits_dR", "dR Separation", 100, 0, 5);
  Hits_delta_eta = fs->make<TH1F>("Hits_delta_eta", "Delta Eta", 100, -1.0, 1.0);
  Hits_delta_phi = fs->make<TH1F>("Hits_delta_phi", "Delta Phi", 100, -1.0, 1.0);
  
  h_GenSep_Crystals = fs->make<TH2F>("h_GenSep_Crystals", "GEN Separation", 100, 0, 25, 100, 0, 25);
  Hits_EB_Centered = fs->make<TH2F>("Hits_EB_Centered", "Centered Pattern", 32, -0.5, 31.5, 32, -0.5, 31.5);
}

DEFINE_FWK_MODULE(ECAL_Simhits_Analyzer);
