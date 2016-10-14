function alpha = GetSlopeAngle(x, iSlope, iDataSet)

if (iDataSet == 1) % Training
    if (iSlope == 1) 
        alpha = 4 + sin(x/20) + cos(sqrt(2)*x/10);   
    elseif (iSlope == 2)
        alpha = 0.3 + sqrt(12./(2+0.1.*(x-5).^2)) + 7./(2+0.1.*(x-20).^2) + sqrt(8./(1+0.01.*(x-81).^2));
    elseif (iSlope == 3)
        alpha = 1 + 100*(sin(x/20)+cos(x/20)).*normpdf(x,500,50) + 200*normpdf(x,50,30);
    elseif (iSlope == 4)
        alpha = 1 + 70*(sin(x/20)+cos(x/20)).*normpdf(x,500,50) + 250*normpdf(x,800,40);
    elseif (iSlope == 5)
        alpha = 0.3 + sqrt(16./(1+0.01.*(x-600).^2)) + 9./(2+0.04.*(x-901).^2) + sqrt(12./(1+0.01.*(x-735).^2));
    elseif (iSlope == 6)
        alpha = 0.3 + sqrt(16./(1+0.01.*(x-20).^2)) + 9./(2+0.04.*(x-78).^2) + sqrt(12./(1+0.005.*(x-46).^2));
    elseif (iSlope == 7)
        alpha = 2 - 150*normpdf(x,104,40) + 250*normpdf(x,307,40);
    elseif (iSlope == 8)
        alpha = 2 - 150*normpdf(x,104,40) + 250*normpdf(x,307,40) - 100*normpdf(x,700,40);
    elseif (iSlope == 9)
        alpha = 1 + 1.7*tanh(0.01*(x-340))- 1.7*tanh(0.01*(x-700)) ;
    elseif (iSlope == 10)
        alpha = 3 + 200*sin(x/50).*(normpdf(x,37,20)+ 3*normpdf(x,700,100)) - (100*normpdf(x,700,40)+0.2).^2;
    end
    
elseif (iDataSet == 2)  % Validation
    if (iSlope == 1) 
        alpha = 4 - sin(x/100) + cos(sqrt(3)*x/50);
    elseif (iSlope == 2)
        alpha = 0.3 + 1.4./(1+0.0001*(x-300).*(x-450)) - 0.02 ./(1+0.0001*(x-365).*(x-560)) + 1.2*(100*normpdf(x,700,40)+0.2).^2;
    elseif (iSlope == 3)
        alpha = 1-0.6./(1+0.0001*(x-300).*(x-450)).*cos(x/70)+ 1.2./(0.3+0.002*(x-460).^2) + 0.5./(0.3+0.002*(x-700).^2) + 0.5./(0.3+0.002*(x-600).^2);
    elseif (iSlope == 4)
        alpha = 1 + 100*(sin(x/20)+cos(x/20)).*normpdf(x,500,50) + 300*normpdf(x,50,30);
    elseif (iSlope == 5) 
        alpha = 5 + sin(x/50) + cos(sqrt(5)*x/50);
    end 
elseif (iDataSet == 3)  % Test
    if (iSlope == 1) 
        alpha = cos(sqrt(3)*x/50) + 5./(0.01*abs(x-400)+1) + 1./(0.01*abs(x-455)+1);
    elseif (iSlope == 2)
        alpha =  1.13 + 120*(sin(x/20)+cos(x/20)).*normpdf(x,500,50) + 2.3./(0.01*abs(x-133)+1);
    elseif (iSlope == 3)
        alpha = 0.5 + 2.3./(0.01*abs(x-133)+1) + 2.3./(0.01*abs(x-166)+1) - 1./(0.01*abs(x-700)+1);
    elseif (iSlope == 4)
        alpha = 4./(1+0.02*x)+0.4 + 1.2*tanh(0.01*(x-137)) + 0.5* sin((x-3)/23) + 0.7*sin((x-50)/87) + 0.4*sin((x-97)/103);
    elseif (iSlope == 5)
        alpha = abs(2.3 + cos(x/68)+0.7*sign(x-433)) -sign(x-671);
    end
end
end