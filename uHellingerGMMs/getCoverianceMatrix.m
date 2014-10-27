function [ covMat ] = getCoverianceMatrix( dimension, diff)
% get a random covariance matrix covMat from inverse-wishart distribution.
% the normal distribution diffiened by N([1,...,1]*diff, covMat) should be
% different enough from the one diffined by N([0,...,0],I) according to Hellinger distance.
% the function samples matrices from the inverse-wishart distribution until
% it finds one that satisfies this criterion. The matrix is save to file.
    DEFAULT_DIMENSION = 100;
    switch nargin
        case 0
           diff = 3;
           dimension = DEFAULT_DIMENSION;
        case 1
           dimension = DEFAULT_DIMENSION;
    end
    
    %sample a matrix from inverse-wishart
    covMat = iwishrnd(eye(dimension), dimension);
    
    %create P0
    pdf0.w = (1);
    pdf0.Mu = (zeros(dimension, 1));
    pdf0.Cov = {eye(dimension)};
    
    %creat P1
    pdf1.w = (1);
    pdf1.Mu = (ones(dimension, 1) * diff);
    pdf1.Cov = {covMat};
    
    %check hellinger distance
    H = uHellingerJointSupport2_ND( pdf0, pdf1 );
    BC = 1 - H*H;
    disp(H);
    disp(BC)
end

