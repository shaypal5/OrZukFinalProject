function [ covMat ] = getCoverianceMatrix( dimension, diff)
% get a random covariance matrix covMat from inverse-wishart distribution.
% the normal distribution diffiened by N([1,...,1]*diff, covMat) should be
% different enough from the one diffined by N([0,...,0],I) according to Hellinger distance.
% the function samples matrices from the inverse-wishart distribution until
% it finds one that satisfies this criterion. The matrix is save to file.
    DEFAULT_DIMENSION = 1000;
    switch nargin
        case 0
           diff = 1.1;
           dimension = DEFAULT_DIMENSION;
        case 1
           dimension = DEFAULT_DIMENSION;
    end
    
    H = 0;
    while H < 0.97
        %sample a matrix from inverse-wishart
        covMat = iwishrnd(eye(dimension), dimension) .* 10^2.5;
        covMat2 = iwishrnd(eye(dimension), dimension);
        disp(det(covMat));
        %create P0
        pdf0.w = (1);
        pdf0.Mu = (ones(dimension, 1));
        pdf0.Cov = {eye(dimension)};
        %pdf0.Cov = {covMat2};

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
end

