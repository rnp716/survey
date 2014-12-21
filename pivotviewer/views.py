from django.http import HttpResponse
from django.shortcuts import redirect
import datetime
import json
import sys

def index(request):
	return redirect('static/index.html')
def current_datetime(request):
	return HttpResponse("hello2")


try:
    from rpy2.robjects import globalEnv
except:
    from rpy2.robjects import globalenv as globalEnv

from rpy2.robjects import r as R1

R1('''
    Result <- function(a,b,c,d,e,z) {
      setwd('/var/www/survey1544/pivotviewer')
      data <- read.csv('test.csv',header=TRUE)
      z <- make.names(z)
      ordered.data <- data[order(eval(parse(text=paste('data$',z)))),]
      frequency.table<-table(eval(parse(text=paste('data$',z)))) 
      vector <- names(frequency.table)
      frequency.array<-as.vector(frequency.table)
      proportion.table<-prop.table(frequency.table)
      proportion.array<-as.vector(proportion.table)
      vector.back <- proportion.array
      copy <- ordered.data
      if(a == 0)
      {
      	x <- rbind(vector, frequency.array, proportion.array)
      }
      if(a != 0)
      {
      	str1 <- strsplit(a,"~")[[1]]
        str.vector1 <- unique(str1)
        header1 <- str.vector1[1]
        header1 <- make.names(header1)
        facet1 <- str.vector1[-1]
        if(length(facet1) > 1)
    	{
          subcopy1 <- copy[eval(parse(text=paste('copy$',header1))) %in% c(facet1),]
    	  frequency.table1<-table((eval(parse(text=paste('subcopy1$',z)))))
    	  #counts of a
          frequency.array1<-as.vector(frequency.table1)
          total.a <- sum(frequency.array1)
    	  proportion.table1<-prop.table(frequency.table1)
    	  proportion.array1<-as.vector(proportion.table1)
    	  r.proportion.array1 <- round(proportion.array1,5)
    	  vector.a <- proportion.array1
        }
        else
        {
          subcopy1 <-subset(copy,eval(parse(text=paste('copy$',header1)))==facet1)
          frequency.table1<-table((eval(parse(text=paste('subcopy1$',z)))))
          frequency.array1<-as.vector(frequency.table1)
          total.a <- sum(frequency.array1)
          proportion.table1<-prop.table(frequency.table1)
          proportion.array1<-as.vector(proportion.table1)
    	  r.proportion.array1 <- round(proportion.array1,5)
          vector.a <- proportion.array1
        }
        if(b==0 && c==0 && d==0 && e==0)
    	{
          vector.acon <-vector.a - vector.back
          r.vector.acon <- round(vector.acon,5)
          percentage.a <- (vector.acon / vector.back)*100
          r.percentage.a <- round(percentage.a,5)
          #vector-names of the different sub-category of toolbar 
          #frequency.array1-counts of a 
          #total.a-total of a 
          #proportion.array1-accuracy of a 
          #vector.acon-contribution of a 
          #percentage.a-contribution of a in percentage 
          x <- rbind(vector,frequency.array1,total.a,r.proportion.array1,r.vector.acon,r.percentage.a)
     	}
      }
 	
      if(b != 0)
      {
     	str2 <- strsplit(b,"~")[[1]]
        str.vector2 <- unique(str2)
        header2 <- str.vector2[1]
        header2 <- make.names(header2)
        facet2 <- str.vector2[-1]
        if(length(facet2) > 1)
    	{
          subcopy2 <- copy[eval(parse(text=paste('copy$',header2))) %in% c(facet2),]
    	  frequency.table2<-table((eval(parse(text=paste('subcopy2$',z)))))
          frequency.array2<-as.vector(frequency.table2)
          total.b <- sum(frequency.array2)
    	  proportion.table2<-prop.table(frequency.table2)
    	  proportion.array2<-as.vector(proportion.table2)
    	  r.proportion.array2 <- round(proportion.array2,5)
    	  vector.b <- proportion.array2 
          subcopy3 <- subcopy1[eval(parse(text=paste('subcopy1$',header2))) %in% c(facet2),]
          frequency.table3 <- table(eval(parse(text=paste('subcopy3$',z))))
    	  frequency.array3 <- as.vector(frequency.table3)
    	  proportion.table3 <- prop.table(frequency.table3)
    	  proportion.array3 <- as.vector(proportion.table3)
    	  vector.ab <- proportion.array3
    	}
        else
        {
          subcopy2 <-subset(copy,eval(parse(text=paste('copy$',header2)))==facet2)
          frequency.table2<-table((eval(parse(text=paste('subcopy2$',z)))))
          frequency.array2<-as.vector(frequency.table2)
          total.b <- sum(frequency.array2)
          proportion.table2<-prop.table(frequency.table2)
          proportion.array2<-as.vector(proportion.table2)
          r.proportion.array2 <- round(proportion.array2,5)
          vector.b <- proportion.array2 
          subcopy3 <- subset(subcopy1, eval(parse(text=paste('subcopy1$', header2)))==facet2)
          frequency.table3 <- table(eval(parse(text=paste('subcopy3$',z))))
    	  frequency.array3 <- as.vector(frequency.table3)
    	  proportion.table3 <- prop.table(frequency.table3)
    	  proportion.array3 <- as.vector(proportion.table3)
    	  vector.ab <- proportion.array3
        }
        if(c==0 && d==0 && e==0)
    	{
    	  #contribution of a to the rules 
    	  vector.acon <- vector.ab - vector.b
    	  r.vector.acon <- round(vector.acon,5)
    	  #percentage 
    	  percentage.a <- (vector.acon / vector.b)*100
    	  r.percentage.a <- round(percentage.a,5)
          #contribution of b to the rules 
          vector.bcon <- vector.ab - vector.a 
          r.vector.bcon <- round(vector.bcon,5)
          #percentage 
          percentage.b <- (vector.bcon / vector.a)*100
          r.percentage.b <- round(percentage.b,5) 
          x <- rbind(vector,frequency.array1,total.a,r.proportion.array1,r.vector.acon,r.percentage.a,frequency.array2,
                     total.b,r.proportion.array2,r.vector.bcon,r.percentage.b)
        }
      }
    
      if(c != 0)
      {
     	str3 <- strsplit(c,"~")[[1]]
        str.vector3 <- unique(str3)
        header3 <- str.vector3[1]
        header3 <- make.names(header3)
        facet3 <- str.vector3[-1]
        if(length(facet3) > 1)
    	{
          subcopy4 <- copy[eval(parse(text=paste('copy$',header3))) %in% c(facet3),]
    	  frequency.table4<-table((eval(parse(text=paste('subcopy4$',z)))))
          frequency.array4<-as.vector(frequency.table4)
          total.c <- sum(frequency.array4)
    	  proportion.table4<-prop.table(frequency.table4)
    	  proportion.array4<-as.vector(proportion.table4)
    	  r.proportion.array4 <- round(proportion.array4,5)
    	  vector.c <- proportion.array4
          subcopy5 <- subcopy3[eval(parse(text=paste('subcopy3$',header3))) %in% c(facet3),]
          subcopy6 <- subcopy1[eval(parse(text=paste('subcopy1$',header3))) %in% c(facet3),]
          subcopy7 <- subcopy2[eval(parse(text=paste('sucopy2$',header3))) %in% c(facet3),]
          frequency.table5 <- table(eval(parse(text=paste('subcopy5$',z))))
    	  frequency.array5 <- as.vector(frequency.table5)
    	  proportion.table5 <- prop.table(frequency.table5)
    	  proportion.array5 <- as.vector(proportion.table5)
    	  vector.abc <- proportion.array5
    	}
        else
        {
          subcopy4 <-subset(copy,eval(parse(text=paste('copy$',header3)))==facet3)
          frequency.table4<-table((eval(parse(text=paste('subcopy4$',z)))))
          frequency.array4<-as.vector(frequency.table4)
          total.c <- sum(frequency.array4)
          proportion.table4<-prop.table(frequency.table4)
          proportion.array4<-as.vector(proportion.table4)
          r.proportion.array4 <- round(proportion.array4,5)
          vector.c <- proportion.array4      
          subcopy5 <- subset(subcopy3, eval(parse(text=paste('subcopy3$', header3)))==facet3)
          subcopy6 <- subset(subcopy1, eval(parse(text=paste('subcopy1$', header3)))==facet3)
          subcopy7 <- subset(subcopy2, eval(parse(text=paste('subcopy2$', header3)))==facet3)
          frequency.table5 <- table(eval(parse(text=paste('subcopy5$',z))))
    	  frequency.array5 <- as.vector(frequency.table5)
    	  proportion.table5 <- prop.table(frequency.table5)
    	  proportion.array5 <- as.vector(proportion.table5)
    	  vector.abc <- proportion.array5
        }
        if(d==0 && e==0)
        {
          frequency.table6 <- table(eval(parse(text=paste('subcopy6$',z))))
    	  frequency.array6 <- as.vector(frequency.table6)
    	  proportion.table6 <- prop.table(frequency.table6)
    	  proportion.array6 <- as.vector(proportion.table6)
    	  vector.ac <- proportion.array6
          frequency.table7 <- table(eval(parse(text=paste('subcopy7$',z))))
    	  frequency.array7 <- as.vector(frequency.table7)
    	  proportion.table7 <- prop.table(frequency.table7)
    	  proportion.array7 <- as.vector(proportion.table7)
    	  vector.bc <- proportion.array7
    	  vector.abc <- proportion.array5
    	  #contribution of a to the rules 
    	  vector.acon <- vector.abc - vector.bc
    	  r.vector.acon <- round(vector.acon,5)
    	  #percentage
    	  percentage.a <- (vector.acon/vector.bc)*100
    	  r.percentage.a <- round(percentage.a,5)
          #contribution of b to the rules 
          vector.bcon <- vector.abc - vector.ac 
          r.vector.bcon <- round(vector.bcon,5)
          #percentage 
          percentage.b <- (vector.bcon/vector.ac)*100
          r.percentage.b <- round(percentage.b, 5)
          #contribution of c to the rules 
          vector.ccon <- vector.abc - vector.ab
          r.vector.ccon <- round(vector.ccon,5)
          #percentage 
          percentage.c <- (vector.ccon/vector.ab)*100
          r.percentage.c <- round(percentage.c, 5)
          x <- rbind(vector,frequency.array1,total.a,r.proportion.array1,r.vector.acon,r.percentage.a,frequency.array2,
                     total.b,r.proportion.array2,r.vector.bcon,r.percentage.b,frequency.array4,total.c,r.proportion.array4,
                     r.vector.ccon,r.percentage.c)
        }
      }
      if(d != 0)
      {
     	str4 <- strsplit(d,"~")[[1]]
        str.vector4 <- unique(str4)
        header4 <- str.vector4[1]
        header4 <- make.names(header4)
        facet4 <- str.vector4[-1]
        if(length(facet4) > 1)
    	{
          subcopy8 <- copy[eval(parse(text=paste('copy$',header4))) %in% c(facet4),]
    	  frequency.table8<-table((eval(parse(text=paste('subcopy8$',z)))))
          frequency.array8<-as.vector(frequency.table8)
          total.d <- sum(frequency.array8)
    	  proportion.table8<-prop.table(frequency.table8)
    	  proportion.array8<-as.vector(proportion.table8)
    	  r.proportion.array8 <- round(proportion.array8,5)
    	  vector.d <- proportion.array8
    	  #subset abd
          subcopy9 <- subcopy3[eval(parse(text=paste('subcopy3$',header4))) %in% c(facet4),]
          #subset bcd
          subcopy10 <- subcopy7[eval(parse(text=paste('subcopy7$',header4))) %in% c(facet4),]
          #subset acd
          subcopy11 <- subcopy6[eval(parse(text=paste('sucopy6$',header4))) %in% c(facet4),]
          #subset abcd 
          subcopy12 <- subcopy5[eval(parse(text=paste('subcopy5$',header4))) %in% c(facet4),]
          frequency.table12 <- table(eval(parse(text=paste('subcopy12$',z))))
    	  frequency.array12 <- as.vector(frequency.table12)
    	  proportion.table12 <- prop.table(frequency.table12)
    	  proportion.array12 <- as.vector(proportion.table12)
    	  vector.abcd <- proportion.array12
    	}
        else
        {
          subcopy8 <-subset(copy,eval(parse(text=paste('copy$',header4)))==facet4)
          frequency.table8<-table((eval(parse(text=paste('subcopy8$',z)))))
          frequency.array8<-as.vector(frequency.table8)
          total.d <- sum(frequency.array8)
          proportion.table8<-prop.table(frequency.table8)
          proportion.array8<-as.vector(proportion.table8)
          r.proportion.array8 <- round(proportion.array8,5)
          vector.d <- proportion.array8   
          #subset abd 
          subcopy9 <- subset(subcopy3, eval(parse(text=paste('subcopy3$', header4)))==facet4)
          #subset bcd 
          subcopy10 <- subset(subcopy7, eval(parse(text=paste('subcopy7$', header4)))==facet4)
          #subset acd 
          subcopy11 <- subset(subcopy6, eval(parse(text=paste('subcopy6$', header4)))==facet4)
          #subset abcd 
          subcopy12 <- subset(subcopy5, eval(parse(text=paste('subcopy5$', header4)))==facet4)
          frequency.table12 <- table(eval(parse(text=paste('subcopy12$',z))))
    	  frequency.array12 <- as.vector(frequency.table12)
    	  proportion.table12 <- prop.table(frequency.table12)
    	  proportion.array12 <- as.vector(proportion.table12)
    	  vector.abcd <- proportion.array12
        }
        if(e==0)
    	{
     	  frequency.table9 <- table(eval(parse(text=paste('subcopy9$',z))))
    	  frequency.array9 <- as.vector(frequency.table9)
    	  proportion.table9 <- prop.table(frequency.table9)
    	  proportion.array9 <- as.vector(proportion.table9)
    	  vector.abd <- proportion.array9
    	  frequency.table10 <- table(eval(parse(text=paste('subcopy10$',z))))
    	  frequency.array10 <- as.vector(frequency.table10)
    	  proportion.table10 <- prop.table(frequency.table10)
    	  proportion.array10 <- as.vector(proportion.table10)
    	  vector.bcd <- proportion.array10
          frequency.table11 <- table(eval(parse(text=paste('subcopy11$',z))))
    	  frequency.array11 <- as.vector(frequency.table11)
    	  proportion.table11 <- prop.table(frequency.table11)
    	  proportion.array11 <- as.vector(proportion.table11)
    	  vector.acd <- proportion.array11
    	  #contribution of a to the rules 
    	  vector.acon <- vector.abcd - vector.bcd
    	  r.vector.acon <- round(vector.acon,5)
    	  #percentage 
    	  percentage.a <- (vector.acon / vector.bcd)*100
    	  r.percentage.a <- round(percentage.a,5)
          #contribution of b to the rules 
          vector.bcon <- vector.abcd - vector.acd 
          r.vector.bcon <- round(vector.bcon,5)
          #percentage 
          percentage.b <- (vector.bcon / vector.acd)*100
          r.percentage.b <- round(percentage.b, 5)
          #contribution of c to the rules 
          vector.ccon <- vector.abcd - vector.abd
          r.vector.ccon <- round(vector.ccon,5)
          #percentage 
          percentage.c <- (vector.ccon / vector.abd)*100
          r.percentage.c <- round(percentage.c,5)
          #contribution of d to the rules
          vector.dcon <- vector.abcd - vector.abc
          r.vector.dcon <- round(vector.dcon,5)
          #percentage 
          percentage.d <- (vector.dcon / vector.abc)*100
          r.percentage.d <- round(percentage.d,5)
          x <- rbind(vector,frequency.array1,total.a,r.proportion.array1,r.vector.acon,r.percentage.a,frequency.array2,
                     total.b,r.proportion.array2,r.vector.bcon,r.percentage.b,frequency.array4,total.c,r.proportion.array4,
                     r.vector.ccon,r.percentage.c,frequency.array8,total.d,r.proportion.array8,r.vector.dcon,
                     r.percentage.d)
        }
      }
      if(e != 0)
      {
     	str5 <- strsplit(e,"~")[[1]]
        str.vector5 <- unique(str5)
        header5 <- str.vector5[1]
        header5 <- make.names(header5)
        facet5 <- str.vector5[-1]
        if(length(facet5) > 1)
    	{
          subcopy13 <- copy[eval(parse(text=paste('copy$',header5))) %in% c(facet5),]
    	  frequency.table13<-table((eval(parse(text=paste('subcopy13$',z)))))
          frequency.array13<-as.vector(frequency.table13)
          total.e <- sum(frequency.array13)
    	  proportion.table13<-prop.table(frequency.table13)
    	  proportion.array13<-as.vector(proportion.table13)
    	  r.proportion.array13 <- round(proportion.array13, 5)
    	  vector.e <- proportion.array13
    	  #subset abde
          subcopy14 <- subcopy9[eval(parse(text=paste('subcopy9$',header5))) %in% c(facet5),]
          #subset bcde
          subcopy15 <- subcopy10[eval(parse(text=paste('subcopy10$',header5))) %in% c(facet5),]
          #subset acde
          subcopy16 <- subcopy11[eval(parse(text=paste('subcopy11$',header5))) %in% c(facet5),]
          #subset abce
          subcopy17 <- subcopy5[eval(parse(text=paste('subcopy5$',header5))) %in% c(facet5),]
          #subset abcde
          subcopy18 <- subcopy12[eval(parse(text=paste('subcopy12$',header5))) %in% c(facet5),]
          frequency.table18 <- table(eval(parse(text=paste('subcopy18$',z))))
    	  frequency.array18 <- as.vector(frequency.table18)
    	  proportion.table18 <- prop.table(frequency.table18)
    	  proportion.array18 <- as.vector(proportion.table18)
    	  vector.abcde <- proportion.array18
    	}
        else
        {
          subcopy13 <-subset(copy,eval(parse(text=paste('copy$',header5)))==facet5)
          frequency.table13<-table((eval(parse(text=paste('subcopy13$',z)))))
          frequency.array13<-as.vector(frequency.table13)
          total.e <- sum(frequency.array13)
          proportion.table13<-prop.table(frequency.table13)
          proportion.array13<-as.vector(proportion.table13)
          r.proportion.array13 <- round(proportion.array13, 5)
          vector.e <- proportion.array13 
          #subset abde 
          subcopy14 <- subset(subcopy9, eval(parse(text=paste('subcopy9$', header5)))==facet5)
          #subset bcde 
          subcopy15 <- subset(subcopy10, eval(parse(text=paste('subcopy10$', header5)))==facet5)
          #subset acde
          subcopy16 <- subset(subcopy11, eval(parse(text=paste('subcopy11$', header5)))==facet5)
          #subset abce
          subcopy17 <- subset(subcopy5, eval(parse(text=paste('subcopy5$', header5)))==facet5)
          #subset abcde
          subcopy18 <- subset(subcopy12, eval(parse(text=paste('subcopy12$', header5)))==facet5)
          frequency.table18 <- table(eval(parse(text=paste('subcopy18$',z))))
    	  frequency.array18 <- as.vector(frequency.table18)
    	  proportion.table18 <- prop.table(frequency.table18)
    	  proportion.array18 <- as.vector(proportion.table18)
    	  vector.abcde <- proportion.array18
        }
        frequency.table14 <- table(eval(parse(text=paste('subcopy14$',z))))
    	  frequency.array14 <- as.vector(frequency.table14)
    	  proportion.table14 <- prop.table(frequency.table14)
    	  proportion.array14 <- as.vector(proportion.table14)
    	  vector.abde <- proportion.array14
    	  frequency.table15 <- table(eval(parse(text=paste('subcopy15$',z))))
    	  frequency.array15 <- as.vector(frequency.table15)
    	  proportion.table15 <- prop.table(frequency.table15)
    	  proportion.array15 <- as.vector(proportion.table15)
    	  vector.bcde <- proportion.array15
          frequency.table16 <- table(eval(parse(text=paste('subcopy16$',z))))
    	  frequency.array16 <- as.vector(frequency.table16)
    	  proportion.table16 <- prop.table(frequency.table16)
    	  proportion.array16 <- as.vector(proportion.table16)
    	  vector.acde <- proportion.array16
          frequency.table17 <- table(eval(parse(text=paste('subcopy17$',z))))
    	  frequency.array17 <- as.vector(frequency.table17)
    	  proportion.table17 <- prop.table(frequency.table17)
    	  proportion.array17 <- as.vector(proportion.table17)
    	  vector.abce <- proportion.array17
    	  #contribution of a to the rules 
    	  vector.acon <- vector.abcde - vector.bcde
    	  r.vector.acon <- round(vector.acon,5)
    	  #percentage 
    	  percentage.a <- (vector.acon/vector.bcde)*100
    	  r.percentage.a <- round(percentage.a, 5)
          #contribution of b to the rules 
          vector.bcon <- vector.abcde - vector.acde
          r.vector.bcon <- round(vector.bcon,5)
          #percentage 
          percentage.b <- (vector.bcon / vector.acde)*100
          r.percentage.b <- round(percentage.b, 5)
          #contribution of c to the rules 
          vector.ccon <- vector.abcde - vector.abde
          r.vector.ccon <- round(vector.ccon,5)
          #percentage 
          percentage.c <- (vector.ccon / vector.abde)*100
          r.percentage.c <- round(percentage.c, 5)
          #contribution of d to the rules 
          vector.dcon <- vector.abcde - vector.abce
          r.vector.dcon <- round(vector.dcon,5)
          #percentage 
          percentage.d <- (vector.dcon / vector.abce)*100
          r.percentage.d <- round(percentage.d, 5)
          #contribution of e to the rules 
          vector.econ <- vector.abcde - vector.abcd
          r.vector.econ <- round(vector.econ,5)
          #percentage 
          percentage.e <- (vector.econ / vector.abcd)*100
          r.percentage.e <- round(percentage.e, 5)
          x <- rbind(vector,frequency.array1,total.a,r.proportion.array1,r.vector.acon,r.percentage.a,frequency.array2,
                     total.b,r.proportion.array2,r.vector.bcon,r.percentage.b,frequency.array4,total.c,r.proportion.array4,
                     r.vector.ccon,r.percentage.c,frequency.array8,total.d,r.proportion.array8,r.vector.dcon,
                     r.percentage.d,frequency.array13,total.e,r.proportion.array13,r.vector.econ,r.percentage.e)
        }
      x <- as.vector(x)
      return(x)
    }
   ''')

def RController(request):
    response_data = {} #create array to store JSON data
    num_facets = 5
    
    facets = json.loads(request.POST.get('facets')) #json.loads un-stringifies
    tb_facet = json.loads(request.POST.get('tb_facet'))
    facets_length = json.loads(request.POST.get('facets_length'))
    print >>sys.stderr, request.POST.get('facets')
    
    if(len(facets) < num_facets):  #if user has selected less than 5 facets
        for j in range(num_facets): #append 0s until array has 5 elements
            facets.append(0)    

    #list(zip(*array)) #use in future?
    #compute the accuracy and contributions
    response_data['results'] = list(R1.Result(facets[0], facets[1], facets[2], 
                                    facets[3], facets[4], tb_facet))

    return HttpResponse(json.dumps(response_data), content_type="application/json")
