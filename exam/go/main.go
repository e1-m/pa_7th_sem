package main

import "fmt"

type BuildingType struct {
	Name    string
	Texture string
	Color   string
}

type BuildingFactory struct {
	types map[string]*BuildingType
}

func NewBuildingFactory() *BuildingFactory {
	return &BuildingFactory{types: make(map[string]*BuildingType)}
}

func (f *BuildingFactory) GetBuildingType(name, texture, color string) *BuildingType {
	key := name + "|" + texture + "|" + color
	if bt, ok := f.types[key]; ok {
		return bt
	}

	bt := &BuildingType{Name: name, Texture: texture, Color: color}
	f.types[key] = bt
	return bt
}

type Building struct {
	X, Y int
	Type *BuildingType
}

func (b *Building) Display() {
	fmt.Printf(
		"Displaying %s at (%d,%d) with %s texture and %s color\n memmory address of the type: %p\n",
		b.Type.Name, b.X, b.Y, b.Type.Texture, b.Type.Color, b.Type)
}

func main() {
	factory := NewBuildingFactory()

	b1 := Building{X: 10, Y: 20, Type: factory.GetBuildingType("House", "Brick", "Red")}
	b2 := Building{X: 15, Y: 25, Type: factory.GetBuildingType("House", "Brick", "Red")}
	b3 := Building{X: 5, Y: 10, Type: factory.GetBuildingType("Shop", "Wood", "Blue")}

	b1.Display()
	b2.Display()
	b3.Display()
}
