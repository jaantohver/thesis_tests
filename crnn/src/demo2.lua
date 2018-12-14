require('cutorch')
require('nn')
require('cunn')
require('cudnn')
require('optim')
require('paths')
require('nngraph')

require('libcrnn')
require('utilities')
require('inference')
require('CtcCriterion')
require('DatasetLmdb')
require('LstmLayer')
require('BiRnnJoin')
require('SharedParallelTable')

require 'lfs'

cutorch.setDevice(1)
torch.setnumthreads(4)
torch.setdefaulttensortype('torch.FloatTensor')

print('Loading model...')
local modelDir = '../model/crnn_demo/'
paths.dofile(paths.concat(modelDir, 'config.lua'))
local modelLoadPath = paths.concat(modelDir, 'crnn_demo_model.t7')
gConfig = getConfig()
gConfig.modelDir = modelDir
gConfig.maxT = 0
local model, criterion = createModel(gConfig)
local snapshot = torch.load(modelLoadPath)
loadModelState(model, snapshot)
model:evaluate()
print(string.format('Model loaded from %s', modelLoadPath))

function dirtree(dir)
	assert(dir and dir ~= "", "directory parameter is missing or empty")
	if string.sub(dir, -1) == "/" then
		dir=string.sub(dir, 1, -2)
    end

	local function yieldtree(dir)
        for entry in lfs.dir(dir) do
			if entry ~= "." and entry ~= ".." then
            	entry=dir.."/"..entry
    			local attr=lfs.attributes(entry)
    			coroutine.yield(entry,attr)
    			if attr.mode == "directory" then
    	  			yieldtree(entry)
    			end
          	end
        end
    end

    return coroutine.wrap(function() yieldtree(dir) end)
end

function getFileName(str)
  	return str:match( "([^/]+)$" )
end

local count = 0.0
local accurate = 0.0

for filename, attr in dirtree("../../cutouts_blur") do
	--local imagePath = '../data/demo.png'
	--local imagePath = '/home/j/Desktop/OCR-Benchmark-images/eng-scan-100-dpi-2.jpg'

	if (attr.mode == 'file') then
		local imagePath = filename
		local iter = string.gmatch(getFileName(imagePath), '([^.]+)')
		local fileName = iter()
		local ext = iter()

		if (ext == 'jpg') then
			local img = loadAndResizeImage(imagePath)

			if (img ~= nil) then
				local text, raw = recognizeImageLexiconFree(model, img)

				--lex = {"elamisluba", "nimi", "kehtivkuni", "valjaandmisekohtjakuupaev", "loaliik", "elamislubatootamiseks", "markused", "residencepermit", "foremployment", "kuni", "until"}

				--local text = recognizeImageWithLexicion(model, img, lex)

				file = io.open("../../crnn_results/srn_out" .. fileName .. ".txt", "w")
				file:write(text)
				file:close()

				count = count + 1.0

				--if (text ~= real) then
				--	print(string.format('Recognized text: %s (raw: %s)', text, raw))
				--	print(string.format('Should be %s', real))
				--	print("-------------------")
				--else
				--	accurate = accurate + 1.0
				--	local percent = accurate * 100.0 / count
				--	print(string.format('Accuracy %02f percent', percent))
				--end

				--print(attr.mode, filename)
			end
		end
	end
end