import ROOT
from DataFormats.FWLite import Events, Handle

# Store the filename in a variable so it's easy to change
file_to_process = 'file:DP1_folder/sample_paper_data_M1_1k_events_DIGI.root'

# Print the filename to the terminal at the start
print '--------------------------------------------------'
print 'Processing File: {}'.format(file_to_process)
print '--------------------------------------------------'

events = Events(file_to_process)
handle = Handle('std::vector<PileupSummaryInfo>')
label = ('addPileupInfo')

for i, event in enumerate(events):
    try:
        event.getByLabel(label, handle)
        pu_infos = handle.product()
        for pu in pu_infos:
            if pu.getBunchCrossing() == 0:
                print 'Event {}: True NPU = {}'.format(i, pu.getTrueNumInteractions())
    except:
        print 'Event {}: Pileup info not found.'.format(i)

    if i >= 5: 
        print '--------------------------------------------------'
        print 'Finished checking first five events.'
        break
