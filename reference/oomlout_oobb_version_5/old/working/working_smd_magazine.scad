
//importing
/*
projection(){
    intersection(){
        import("working_smd_magazine.stl");
            translate([0,0,6]){
                cube(size=[1000,1000,0.1]);
        }
    }
}
*/

difference(){
    translate([-1,-1,0]){
        cube([25,8,2]);
    }
        
    linear_extrude(0.3){
        import("working_smd_magazine_1.svg");
        }
    }