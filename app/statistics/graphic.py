import pandas as pd
import plotly.graph_objects as go
import glob
import os


def addDatasInDatasPD(objectRequestDB, typeGraphic):

    objectDatasPD = {
        'energy': {},
        'water': {}
    }

    for data in objectRequestDB:

        if data.mote.get_type_display() == 'EMote':

            if typeGraphic == "raw":

                dataMoteName = data.mote.name
                dataCollectDate = data.collect_date
                dataLastCollection = data.last_collection

                try:

                    objectDatasPD['energy'][dataMoteName] = [[* objectDatasPD['energy'][dataMoteName][0],
                                                              dataCollectDate], [* objectDatasPD['energy'][dataMoteName][1], dataLastCollection]]
                except:
                    objectDatasPD['energy'][dataMoteName] = [[], []]
                    objectDatasPD['energy'][dataMoteName][0].append(
                        dataCollectDate)
                    objectDatasPD['energy'][dataMoteName][1].append(
                        dataLastCollection)

            elif typeGraphic == "1h1mean":

                mean = data.mean
                dataMoteName = data.mote.name
                dateMean = data.created_at

                try:

                    objectDatasPD['energy'][dataMoteName] = [[* objectDatasPD['energy'][dataMoteName][0],
                                                              dateMean], [* objectDatasPD['energy'][dataMoteName][1], mean]]
                except:
                    objectDatasPD['energy'][dataMoteName] = [[], []]
                    objectDatasPD['energy'][dataMoteName][0].append(
                        dateMean)
                    objectDatasPD['energy'][dataMoteName][1].append(
                        mean)

        elif data.mote.get_type_display() == 'WMote':

            if typeGraphic == "raw":

                dataMoteName = data.mote.name
                dataCollectDate = data.collect_date
                dataLastCollection = data.last_collection

                try:
                    objectDatasPD['water'][dataMoteName] = [[* objectDatasPD['water'][dataMoteName][0],
                                                            dataCollectDate], [* objectDatasPD['water'][dataMoteName][1], dataLastCollection]]
                except:
                    objectDatasPD['water'][dataMoteName] = [[], []]
                    objectDatasPD['water'][dataMoteName][0].append(
                        dataCollectDate)
                    objectDatasPD['water'][dataMoteName][1].append(
                        dataLastCollection)

            elif typeGraphic == "1h1mean":

                mean = data.mean
                dataMoteName = data.mote.name
                dateMean = data.created_at

                try:

                    objectDatasPD['water'][dataMoteName] = [[* objectDatasPD['water'][dataMoteName][0],
                                                             dateMean], [* objectDatasPD['water'][dataMoteName][1], mean]]
                except:
                    objectDatasPD['water'][dataMoteName] = [[], []]
                    objectDatasPD['water'][dataMoteName][0].append(
                        dateMean)
                    objectDatasPD['water'][dataMoteName][1].append(
                        mean)

        else:
            pass

    return objectDatasPD


def createDataFrame(objectDatas, pathToCreateArchive):
    typeEnergy = 'energy'
    typeWater = 'water'
    getNameMote = 0
    getArrayDatas = 1
    getDatesInArrayDatas = 0
    getValuesInArrayDatas = 1

    for energyItems in objectDatas[typeEnergy].items():

        dataFrameCreateEnergy = pd.DataFrame(
            {'Data': energyItems[getArrayDatas][getDatesInArrayDatas], 'Valor': energyItems[getArrayDatas][getValuesInArrayDatas]})

        createPlotly(dataFrameCreateEnergy,
                     energyItems[getNameMote], pathToCreateArchive)

    for waterItems in objectDatas[typeWater].items():
        dataFrameCreateWater = pd.DataFrame(
            {'Data': waterItems[getArrayDatas][getDatesInArrayDatas], 'Valor': waterItems[getArrayDatas][getValuesInArrayDatas]})

        createPlotly(dataFrameCreateWater,
                     waterItems[getNameMote], pathToCreateArchive)


def createPlotly(arrayToPlotly, nameToFileCreate, pathToCreateFile):

    templateHoverWater = '<i>Data</i>: %{x}' + \
        '<br><i>Consumo(L)</i>: %{y:.1f}L <extra></extra>'

    templateHoverEnergy = '<i>Data</i>: %{x}' + \
        '<br><i>Consumo(W)</i>: %{y:.1f}W <extra></extra>'

    if nameToFileCreate[0] in 'Ee':
        createPlotly = go.Figure(go.Scatter(
            x=arrayToPlotly['Data'],
            y=arrayToPlotly['Valor'],
            mode='markers+lines',
            hovertemplate=templateHoverEnergy))

        createPlotly.update_layout(

            title='',
            xaxis=dict(
                title='',
                showticklabels=False,),
            yaxis=dict(
                title='',
                showticklabels=False,
            ),
            margin=dict(l=0, r=0, t=0, b=0, pad=100),
        )

        createPlotly.write_html(
            f"{pathToCreateFile}/energy/{nameToFileCreate}.html")

    elif nameToFileCreate[0] in 'Ww':
        createPlotly = go.Figure(go.Scatter(
            x=arrayToPlotly['Data'],
            y=arrayToPlotly['Valor'],
            mode='markers+lines',
            hovertemplate=templateHoverWater))

        createPlotly.update_layout(

            title='',
            xaxis=dict(
                title='',
                showticklabels=False,),
            yaxis=dict(
                title='',
                showticklabels=False,
            ),
            margin=dict(l=0, r=0, t=0, b=0, pad=100),
        )

        createPlotly.write_html(
            f"{pathToCreateFile}/water/{nameToFileCreate}.html")
    else:
        pass


def addGraphicsInHTML(pathSearchArchives):
    searchHTMLFiles = glob.glob(
        f'{pathSearchArchives}/**/*.html', recursive=True)
    

    arrayPathForIframes = []
    arrayNameForHTML = []

    for HTMLFile in searchHTMLFiles:
        HTMLPath = HTMLFile.replace('.html', '').replace('/', '-').replace('app-templates-graphics-dashboard-', 'graphic/')
        HTMLFileName = HTMLPath.replace('graphic/', '')
        arrayPathForIframes.append(f'/{HTMLPath}')
        arrayNameForHTML.append(HTMLFileName)

    return [arrayPathForIframes, arrayNameForHTML]


def mainGraphics(datas, pathToCreateArchive, pathToSearchArquives, typeGraphic):
    datasInPd = addDatasInDatasPD(datas, typeGraphic)
    createDataFrame(datasInPd, pathToCreateArchive) 
    graphics = addGraphicsInHTML(pathToSearchArquives)
    return graphics
