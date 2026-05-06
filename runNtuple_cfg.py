import FWCore.ParameterSet.Config as cms

process = cms.Process("NTUPLE")

# Load standard geometry and magnetic field for the Ntuplerizer
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v11_L1v1', '')

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:DP1_folder/sample_paper_data_M1_1k_events_RECO.root')
)

# Define the Ntuplerizer module based on your .cc class
process.ntupler = cms.EDAnalyzer("Photon_RefinedRecHit_NTuplizer",
    isMC = cms.bool(True),
    miniAODRun = cms.bool(False),
    useOuterHits = cms.bool(False), # Set to False to stop the crash
    photons = cms.InputTag("photons"),
    genParticles = cms.InputTag("genParticles"),
    rhoFastJet = cms.InputTag("fixedGridRhoFastjetAll"),
    # Comment out or use dummy paths since useOuterHits is False
    ebNeighbourXtalMap = cms.FileInPath("Analyzer/EcalMapping/plugins/Photon_RefinedRecHit_NTuplizer.cc"), 
    eeNeighbourXtalMap = cms.FileInPath("Analyzer/EcalMapping/plugins/Photon_RefinedRecHit_NTuplizer.cc"),
    eleMediumIdMap = cms.InputTag(""),
    eleTightIdMap = cms.InputTag("")
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("DP1_folder/sample_paper_data_M1_1k_events_Ntuple.root")
)

process.p = cms.Path(process.ntupler)
