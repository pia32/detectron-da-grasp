% this script resize the Jacquard grasping dataset into small sizes
% the original size is 1024x1024 and the processed dataset is 512x512

% resize RGB, MASK, DEPTH, STEREO
% recompute grasps
% generate RGD
% generate unrotated bounding boxes, class

%% clean environment
clear;
close all;

%% user specified data path (I/O)
DATA_DIR = '/local/patrick/datasets/jac_small';
DATA_DIR_OUT = '/local/patrick/datasets/jac_resized';
SCALE = 0.5;

%% main processing
listFolder = dir(DATA_DIR);

% 11 folders, each with 1000 subfolders
for idxFolder = 3:length(listFolder)
   nameFolder = listFolder(idxFolder).name;
   fprintf(['processing.. ' nameFolder '\n']); 
   
   % 1000 subfolders
   listSubfolder = dir(fullfile(DATA_DIR, nameFolder));
   for idxSubfolder = 3:length(listSubfolder)
       nameSubfolder = listSubfolder(idxSubfolder).name;
       
       subfolderPath = fullfile(DATA_DIR_OUT, nameFolder, nameSubfolder);
       if exist(subfolderPath, 'dir')
           fprintf('folder exists'); 
       else
           mkdir(subfolderPath);
       end

       % process GT inside the folder
       listRGB = dir(fullfile(DATA_DIR, nameFolder, nameSubfolder,'*_RGB.png'));
       for idxImg = 1:length(listRGB)
           nameImg = listRGB(idxImg).name;
           nameDepth = strrep(nameImg, '_RGB.png', '_stereo_depth.tiff');
           nameMask = strrep(nameImg, '_RGB.png', '_mask.png');
           nameGT = strrep(nameImg, '_RGB.png', '_grasps.txt');
           nameRGD = strrep(nameImg, '_RGB.png', '_RGD.png');
           
           % read rgb/depth/mask
           rgbImg = imread(fullfile(DATA_DIR, nameFolder, nameSubfolder, nameImg));
           depthImg = imread(fullfile(DATA_DIR, nameFolder, nameSubfolder, nameDepth));
           maskImg = imread(fullfile(DATA_DIR, nameFolder, nameSubfolder, nameMask));
            
           % resize rgb/depth/mask
           rgbImg_resized = imresize(rgbImg,SCALE,'method','bilinear');
           depthImg_resized = imresize(depthImg,SCALE,'method','bilinear');
           maskImg_resized = imresize(maskImg,SCALE,'method','bilinear');
           depthImg_resized(depthImg_resized < 0) = -1;
           maskImg_resized(maskImg_resized > 128) = 255; maskImg_resized(maskImg_resized <= 128) = 0;

           % write rgb/depth/mask
           imwrite(rgbImg_resized, fullfile(DATA_DIR_OUT, nameFolder, nameSubfolder, nameImg));
           imwrite(double(depthImg_resized), fullfile(DATA_DIR_OUT, nameFolder, nameSubfolder, nameDepth), 'tiff');
           imwrite(maskImg_resized, fullfile(DATA_DIR_OUT, nameFolder, nameSubfolder, nameMask));

           % generate RGD
           if max(max(depthImg_resized)) > 1.90, fprintf(['1.90 warning: ' num2str(max(max(depthImg_resized)))   '\n']); end
           depthImg_resized = double((depthImg_resized-1.40))/(1.90-1.40)*255;
           depthImg_resizedUint = uint8(depthImg_resized);
           rgbImg_resized(:,:,3) = depthImg_resizedUint;
           imwrite(rgbImg_resized, fullfile(DATA_DIR_OUT, nameFolder, nameSubfolder, nameRGD));
           
           gtFile = fopen(fullfile(DATA_DIR, nameFolder, nameSubfolder, nameGT));
           gtCell = textscan(gtFile, '%f;%f;%f;%f;%f');
           fclose(gtFile);
           outGtFile = fopen(fullfile(DATA_DIR_OUT, nameFolder, nameSubfolder, nameGT),'w');
           for idxGrasp = 1: length(gtCell{1})
               x = gtCell{1}(idxGrasp)/2;
               y = gtCell{2}(idxGrasp)/2;
               theta = gtCell{3}(idxGrasp);
               open = gtCell{4}(idxGrasp)/2;
               size = gtCell{5}(idxGrasp)/2;
               cls = orientationClass(theta);
               bbox_ul_x = x - open/2;
               bbox_br_x = x + open/2;
               bbox_ul_y = y - size/2;
               bbox_br_y = y + size/2;
               fprintf(outGtFile, [num2str(x) ';' num2str(y) ';' num2str(theta) ';' num2str(open) ';' num2str(size) ';' num2str(cls) ';' num2str(bbox_ul_x) ';' num2str(bbox_ul_y) ';' num2str(bbox_br_x) ';' num2str(bbox_br_y) '\n']);
           end

           fclose(outGtFile);

           
       end
   end
    
end

function cls = orientationClass(theta_in_degree)
    theta_in_degree = theta_in_degree + 90 + 2.5;
    cls = theta_in_degree/5;
    cls = floor(cls);
    if cls == 0
        cls = 36;
    end
   
end