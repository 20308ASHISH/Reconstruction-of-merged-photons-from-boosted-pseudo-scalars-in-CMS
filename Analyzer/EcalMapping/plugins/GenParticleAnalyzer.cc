#include <memory>
#include <vector>
#include <algorithm>
#include <iostream>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "SimDataFormats/CaloHit/interface/PCaloHit.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "TH2F.h"

class GenParticleAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit GenParticleAnalyzer(const edm::ParameterSet&);
private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<std::vector<PCaloHit>> ebHitsToken_;
  edm::EDGetTokenT<reco::GenParticleCollection> genToken_;
  TH2F *h_paper_final; 
};

GenParticleAnalyzer::GenParticleAnalyzer(const edm::ParameterSet& iConfig) {
  usesResource("TFileService");
  
  // Consumes the tags defined in the Python config
  ebHitsToken_ = consumes<std::vector<PCaloHit>>(iConfig.getParameter<edm::InputTag>("ecalHitsEB"));
  genToken_ = consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles"));

  edm::Service<TFileService> fs;
  
  // Mapping the full ECAL Barrel
  // iEta: -85 to 85 (171 bins) | iPhi: 1 to 360 (360 bins)
  h_paper_final = fs->make<TH2F>("h_paper_final", 
                                 "Full ECAL Detector Map; i#eta; i#phi", 
                                 171, -85.5, 85.5, 360, 0.5, 360.5);
}

void GenParticleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  
  // 1. Terminal Printout: The Generator Truth
  auto const& genParticles = iEvent.get(genToken_);
  std::cout << "\n>>> EVENT " << iEvent.id().event() << " GEN PARTICLE CHECK <<<" << std::endl;
  
  for (const auto& p : genParticles) {
    // pdgId 22 is Photon, Status 1 is final state
    if (p.status() == 1 && p.pdgId() == 22) {
      std::cout << "  Photon Found -> E: " << p.energy() 
                << " | Eta: " << p.eta() 
                << " | Phi: " << p.phi() << std::endl;
    }
  }

  // 2. Hit Analysis: The Detector Response
  auto const& ebHits = iEvent.get(ebHitsToken_);
  
  if (!ebHits.empty()) {
    for (const auto& hit : ebHits) {
      EBDetId id(hit.id());
      // Fill the histogram using the absolute crystal indices
      h_paper_final->Fill(id.ieta(), id.iphi(), hit.energy());
    }
  }
}

DEFINE_FWK_MODULE(GenParticleAnalyzer);