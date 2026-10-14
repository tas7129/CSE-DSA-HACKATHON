package edu.demo.exam.algorithm;

import edu.demo.exam.model.*;import edu.demo.exam.util.TimetableValidator;import java.util.*;

/** Deterministic DSatur: highest saturation, then degree, then lowest course id. */
public final class DSaturSolver {
    public Timetable solve(ConflictGraph g,int capacity){if(capacity<1)throw new IllegalArgumentException("Hall capacity must be positive.");long start=System.nanoTime();int n=g.size();int[] c=new int[n];Arrays.fill(c,-1);int[] counts=new int[n];List<Integer> order=new ArrayList<>();int used=0;
        for(int step=0;step<n;step++){int v=-1,bestSat=-1,bestDegree=-1;for(int x=0;x<n;x++)if(c[x]<0){Set<Integer>s=new HashSet<>();for(int y:g.neighbours(x+1))if(c[y]>=0)s.add(c[y]);if(s.size()>bestSat||(s.size()==bestSat&&(g.degree(x+1)>bestDegree||(g.degree(x+1)==bestDegree&&x<v)))){v=x;bestSat=s.size();bestDegree=g.degree(x+1);}}
            boolean[] forbidden=new boolean[used];for(int y:g.neighbours(v+1))if(c[y]>=0)forbidden[c[y]]=true;int color=0;while(color<used&&(forbidden[color]||counts[color]>=capacity))color++;if(color==used)used++;c[v]=color;counts[color]++;order.add(v+1);
        }Timetable t=new Timetable(c,System.nanoTime()-start,false,false,order);TimetableValidator.requireValid(g,capacity,t);return t;}
}
