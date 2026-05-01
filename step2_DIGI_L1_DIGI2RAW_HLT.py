# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --datatier GEN-SIM-DIGI-RAW-HLTDEBUG --conditions auto:run1_mc -s DIGI:pdigi_valid,L1,DIGI2RAW,HLT:@fake --eventcontent FEVTDEBUGHLT -n 100 --filein file:step1.root --fileout file:step2.root
import FWCore.ParameterSet.Config as cms



process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_Fake_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring('file:DP1_folder/AToGG_GEN_E0.5_new.root'),
    inputCommands = cms.untracked.vstring(
        'keep *' 
        # 'drop *_genParticles_*_*', 
        # 'drop *_genParticlesForJets_*_*', 
        # 'drop *_kt4GenJets_*_*', 
        # 'drop *_kt6GenJets_*_*', 
        # 'drop *_iterativeCone5GenJets_*_*', 
        # 'drop *_ak4GenJets_*_*', 
        # 'drop *_ak7GenJets_*_*', 
        # 'drop *_ak8GenJets_*_*', 
        # 'drop *_ak4GenJetsNoNu_*_*', 
        # 'drop *_ak8GenJetsNoNu_*_*', 
        # 'drop *_genCandidatesForMET_*_*', 
        # 'drop *_genParticlesForMETAllVisible_*_*', 
        # 'drop *_genMetCalo_*_*', 
        # 'drop *_genMetCaloAndNonPrompt_*_*', 
        # 'drop *_genMetTrue_*_*', 
        # 'drop *_genMetIC5GenJs_*_*'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# for mixing
with open('input_to_aviks_pythoncode.txt') as f:
    file_list = [line.strip() for line in f if line.strip()]
process.mix.input = cms.SecSource("PoolSource",
    fileNames = cms.untracked.vstring(*file_list),

    nbPileupEvents = cms.PSet(
        probFunctionVariable = cms.vint32(0,1,2,3,4,5,10,20),
        probValue = cms.vdouble(0.01,0.01,0.02,0.05,0.1,0.2,0.3,0.31)   # how to define this , i choose the random value
    )
)
process.mix.input.type = cms.string('probFunction')
process.mix.bunchspace = cms.int32(50)


# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)


# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW-HLTDEBUG'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:DP1_folder/AToGG_GEN_E0.5_new_DIGI.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    # splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.mix.digitizers = cms.PSet(process.theDigitizersValid)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run1_mc', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.FEVTDEBUGHLToutput_step])
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
