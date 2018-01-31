
VPATH = ../../conf:../../lib/chemicalGraph ../classifier ../nanotubeEditor ../homopolyEditor

Wolffia.py: ui_Wolffia.py Wolffia_conf.py BuildTab.py SetupTab.py ForceTab.py Analysis.py AboutFT.py SimTab.py MinTab.py History.py Drawer.py SettingsDialog.py SolventDialog.py Wolffia_icons_rc.py MixtureBrowser.py LogWindow.py ConnectionDialog.py

ui_Wolffia.py: wolffia.ui
	pyuic4 wolffia.ui -o ui_Wolffia.py

SimTab.py: Wolffia_conf.py ui_BuildTab.py ui_SimTab.py MixtureViewer.py MinTab.py

MixtureBrowser.py: Wolffia_conf.py ChemicalGraph.py MixtureViewer.py ui_MixtureBrowser.py History.py 

ui_MixtureBrowser.py: MixtureBrowser.ui
	pyuic4 MixtureBrowser.ui -o ui_MixtureBrowser.py

ui_SimTab.py: simTab.ui
	pyuic4 simTab.ui -o ui_SimTab.py
	sed -e 's/qwt_analog_clock/PyQt4.Qwt5/' ui_SimTab.py > /tmp/ui_SimTab.py
	sed -e 's/qwt_plot/PyQt4.Qwt5/' /tmp/ui_SimTab.py > /tmp/ui_SimTab2.py
	sed -e 's/qwt_thermo/PyQt4.Qwt5/' /tmp/ui_SimTab2.py > ui_SimTab.py
	rm /tmp/ui_SimTab.py /tmp/ui_SimTab2.py

MinTab.py: Wolffia_conf.py ui_MinTab.py MixtureViewer.py

ui_MinTab.py: minTab.ui
	pyuic4 minTab.ui -o ui_MinTab.py
	sed -e 's/qwt_analog_clock/PyQt4.Qwt5/' ui_MinTab.py > /tmp/ui_MinTab.py
	sed -e 's/qwt_plot/PyQt4.Qwt5/' /tmp/ui_MinTab.py > ui_MinTab.py
	rm /tmp/ui_MinTab.py 


BuildTab.py: ui_BuildTab.py Wolffia_conf.py ChemicalGraph.py StructureManagerWidget.py PropertyEditor.py MixtureViewer.py \
             Load.py nanotubeEditor.py HomopolyEditor.py

ui_BuildTab.py: buildTab.ui
	pyuic4 buildTab.ui -o ui_BuildTab.py
	sed -e 's/qwt_analog_clock/PyQt4.Qwt5/' ui_BuildTab.py > /tmp/ui_BuildTab.py
	sed -e 's/qwt_plot/PyQt4.Qwt5/' /tmp/ui_BuildTab.py > ui_BuildTab.py
	rm /tmp/ui_BuildTab.py

Drawer.py: Wolffia_conf.py

ForceTab.py: ui_ForceTab.py Wolffia_conf.py MixtureViewer.py ui_CHARMMParameterFinderDialog.py

ui_ForceTab.py:  forceTab.ui
	pyuic4 -o ui_ForceTab.py forceTab.ui

Analysis.py: ui_Analysis.py

ui_Analysis.py:  Analysis.ui
	pyuic4 -o ui_Analysis.py Analysis.ui

AboutFT.py: ui_AboutFT.py Wolffia_conf.py 

ui_AboutFT.py: aboutFt.ui
	pyuic4 -o ui_AboutFT.py aboutFt.ui

MixtureViewer.py: GeometricObjects.py ChemicalGraph.py

History.py: Wolffia_conf.py ChemicalGraph.py

PropertyEditor.py: ui_PropertyEditor.py ChemicalGraph.py

ui_PropertyEditor.py: propertyEditor.ui
	pyuic4 -o ui_PropertyEditor.py propertyEditor.ui

SetupTab.py: ui_SetupTab.py Wolffia_conf.py ChemicalGraph.py MixtureViewer.py

ui_SetupTab.py: setupTab.ui
	pyuic4 -o ui_SetupTab.py setupTab.ui

SettingsDialog.py: ui_SettingsDialog.py Wolffia_conf.py 

ui_SettingsDialog.py: settingsDialog.ui
	pyuic4 -o ui_SettingsDialog.py settingsDialog.ui

setDialMixture.py: ui_setDialMixture.py Wolffia_conf.py 

ui_setDialMixture.py: setDialMixture.ui
	pyuic4 -o ui_setDialMixture.py setDialMixture.ui

SolventDialog.py: ui_SolventDialog.py Wolffia_conf.py 

ui_SolventDialog.py: solventDialog.ui
	pyuic4 -o ui_SolventDialog.py solventDialog.ui

ConnectionDialog.py: ui_ConnectionDialog.py Wolffia_conf.py 

ui_ConnectionDialog.py: ConnectionDialog.ui
	pyuic4 -o ui_ConnectionDialog.py ConnectionDialog.ui

LogWindow.py: Wolffia_conf.py 

ui_CHARMMParameterFinderDialog.py: CHARMMParameterFinderDialog.ui
	pyuic4 -o ui_CHARMMParameterFinderDialog.py CHARMMParameterFinderDialog.ui
	sed -e 's/qwt_analog_clock/PyQt4.Qwt5/' ui_CHARMMParameterFinderDialog.py > /tmp/ui_CHARMMParameterFinderDialog.py
	cp /tmp/ui_CHARMMParameterFinderDialog.py  ui_CHARMMParameterFinderDialog.py
	sed -e 's/qwt_dial/PyQt4.Qwt5/' ui_CHARMMParameterFinderDialog.py > /tmp/ui_CHARMMParameterFinderDialog.py
	sed -e 's/qwt_plot/PyQt4.Qwt5/' /tmp/ui_CHARMMParameterFinderDialog.py > ui_CHARMMParameterFinderDialog.py
	rm /tmp/ui_CHARMMParameterFinderDialog.py


StructureManagerWidget.py: Wolffia_conf.py

Wolffia_icons_rc.py: Wolffia_icons.qrc
	pyrcc4 Wolffia_icons.qrc -o Wolffia_icons_rc.py

clean:
	rm -f *.pyc *.py~ ui_*.py

