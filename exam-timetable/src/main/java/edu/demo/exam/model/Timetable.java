package edu.demo.exam.model;

import java.util.*;

/** Immutable result with zero-based slot ids and one-based course ids. */
public final class Timetable {
    private final int[] slots; private final long elapsedNanos; private final boolean optimal; private final boolean timedOut; private final List<Integer> order;
    public Timetable(int[] slots,long elapsedNanos,boolean optimal,boolean timedOut,List<Integer> order){this.slots=slots.clone();this.elapsedNanos=elapsedNanos;this.optimal=optimal;this.timedOut=timedOut;this.order=List.copyOf(order);}
    public int[] assignments(){return slots.clone();} public int slotCount(){return Arrays.stream(slots).max().orElse(-1)+1;} public long elapsedNanos(){return elapsedNanos;} public double elapsedMillis(){return elapsedNanos/1_000_000.0;} public boolean optimal(){return optimal;} public boolean timedOut(){return timedOut;} public List<Integer> assignmentOrder(){return order;}
    public List<List<Integer>> bySlot(){List<List<Integer>> out=new ArrayList<>();for(int i=0;i<slotCount();i++)out.add(new ArrayList<>());for(int i=0;i<slots.length;i++)if(slots[i]>=0)out.get(slots[i]).add(i+1);return out.stream().map(List::copyOf).toList();}
}
