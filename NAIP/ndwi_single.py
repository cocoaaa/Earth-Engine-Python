import ee
import ee.mapclient

ee.Initialize()
lat = 46.80514
lng = -99.22023

image = ee.Image('USDA/NAIP/DOQQ/m_4609915_sw_14_1_20100629')

vis = {'bands': ['N', 'R', 'G']}
ee.mapclient.centerMap(lng, lat, 13)
ee.mapclient.addToMap(image, vis)

ndwi = image.normalizedDifference(['G', 'N'])
ndwiViz = {'min': 0.2, 'max': 1, 'palette': ['00FFFF', '0000FF']}
ndwiMasked = ndwi.updateMask(ndwi.gte(0.2))
ndwi_bin = ndwiMasked.gt(0)
ee.mapclient.addToMap(ndwiMasked, ndwiViz)

# Image.connectedPixelCount(maxSize, eightConnected)                                                    
# #maxSize means that any region equal or larger than the maxSize will be assigned a value to the maxSize.
patch_size = ndwi_bin.connectedPixelCount(1000, True)
# ee.mapclient.addToMap(patch_size)

large_patches = patch_size.eq(1000)
large_patches = large_patches.updateMask(large_patches)
# ee.mapclient.addToMap(large_patches)

patch_id = large_patches.connectedComponents(ee.Kernel.plus(1), 256)
ee.mapclient.addToMap(patch_id)

# downConfig = {'scale':30, "maxPixels": 1.0E13, 'driveFolder':'test', 'CRS': 'EPGS:31983', 'region': roiExample }
#
# task = ee.batch.Export.image(image.select( ['B2', 'B3' ,'B4', 'B5',  'B6']).toDouble(), 'sirgas20023sPy', downConfig)
# task.start()                                                                                                                                                                                                                                                       


# #
downConfig = {'scale': 5, "maxPixels": 1.0E13, 'driveFolder': 'image'}  # scale means resolution.
# task = ee.batch.Export.image(image, "naip", downConfig)
# task.start()
# task = ee.batch.Export.image(patch_size, "patch_size", downConfig)
# task.start()
# task = ee.batch.Export.image(large_patches, "large_patches", downConfig)
# task.start()
task = ee.batch.Export.image(patch_id.toInt32(), "patch_id", downConfig)
task.start()
