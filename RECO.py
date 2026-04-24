import FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

# --- ALIGNED STANDARD SEQUENCES ---
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# --- OPTIONS (Fixes the ConfigFileReadError) ---
process.options = cms.untracked.PSet()

# --- INPUT SOURCE ---
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:DP1_folder/sample_paper_data_M0.1_1k_events_DIGI.root'),
    secondaryFileNames = cms.untracked.vstring()
)

# --- GLOBAL TAG ALIGNMENT ---
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run1_mc', '')

# --- OUTPUT DEFINITION ---
process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RECO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:DP1_folder/sample_paper_data_M0.1_1k_events_RECO.root'),
    outputCommands = cms.untracked.vstring('keep *'),
    splitLevel = cms.untracked.int32(0)
)

# --- RECO PATHS ---
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# --- SCHEDULE ---
process.schedule = cms.Schedule(
    process.raw2digi_step,
    process.L1Reco_step,
    process.reconstruction_step,
    process.endjob_step,
    process.RECOSIMoutput_step
)

# =========================================================================
# SURGICAL RECO KILL SWITCH (Crucial for 10_6_X Run 1)
# =========================================================================

# 1. Disable GEM/ME0 in Muon Reconstruction
if hasattr(process, 'muons1stStep'):
    process.muons1stStep.FillGEMHits = cms.bool(False)
    process.muons1stStep.FillME0Hits = cms.bool(False)

# 2. Prevent GEM prefetching in Track Associators
if hasattr(process, 'trackAssociatorByHits'):
    process.trackAssociatorByHits.useGEM = cms.bool(False)
    process.trackAssociatorByHits.useME0 = cms.bool(False)

# 3. Clean GEM from local muon reconstruction if it exists in the path
for mod in ['gemRecHits', 'gemSegments', 'me0RecHits', 'me0Segments']:
    if hasattr(process, mod):
        process.reconstruction.remove(getattr(process, mod))

# --- EARLY DELETION (Must be after Paths and Schedule) ---
#from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
#process = customiseEarlyDelete(process)
