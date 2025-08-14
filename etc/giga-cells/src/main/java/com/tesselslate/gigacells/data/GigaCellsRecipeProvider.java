package com.tesselslate.gigacells.data;

import com.tesselslate.gigacells.GigaCells;
import com.tesselslate.gigacells.GigaCellsItems;

import net.minecraft.data.DataProvider;
import net.minecraft.data.PackOutput;
import net.minecraft.data.recipes.FinishedRecipe;
import net.minecraft.data.recipes.RecipeCategory;
import net.minecraft.data.recipes.RecipeProvider;
import net.minecraft.data.recipes.ShapelessRecipeBuilder;
import net.minecraftforge.data.event.GatherDataEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

import java.util.function.Consumer;

@Mod.EventBusSubscriber(modid = GigaCells.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class GigaCellsRecipeProvider extends RecipeProvider {
    public GigaCellsRecipeProvider(PackOutput output) {
        super(output);
    }

    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {
        event.getGenerator().addProvider(event.includeServer(), new DataProvider.Factory<>() {
            @Override
            public GigaCellsRecipeProvider create(PackOutput output) {
                return new GigaCellsRecipeProvider(output);
            }
        });
    }

    @Override
    public void buildRecipes(Consumer<FinishedRecipe> writer) {
        var item_housing_mk1 = GigaCellsItems.ITEM_CELL_HOUSING_MK1;
        var item_housing_mk2 = GigaCellsItems.ITEM_CELL_HOUSING_MK2;
        var fluid_housing_mk1 = GigaCellsItems.FLUID_CELL_HOUSING_MK1;
        var fluid_housing_mk2 = GigaCellsItems.FLUID_CELL_HOUSING_MK2;

        for (int i = 0; i < 5; i++) {
            var gb_component = GigaCellsItems.GIGABYTE_CELL_COMPONENTS[i];
            var tb_component = GigaCellsItems.TERABYTE_CELL_COMPONENTS[i];

            var item_cell_mk1 = GigaCellsItems.GIGABYTE_ITEM_CELLS[i];
            var item_cell_mk2 = GigaCellsItems.TERABYTE_ITEM_CELLS[i];
            var fluid_cell_mk1 = GigaCellsItems.GIGABYTE_FLUID_CELLS[i];
            var fluid_cell_mk2 = GigaCellsItems.TERABYTE_FLUID_CELLS[i];

            ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, item_cell_mk1)
                    .requires(gb_component)
                    .requires(item_housing_mk1)
                    .unlockedBy(getHasName(gb_component), has(gb_component))
                    .save(writer);
            ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, item_cell_mk2)
                    .requires(tb_component)
                    .requires(item_housing_mk2)
                    .unlockedBy(getHasName(gb_component), has(tb_component))
                    .save(writer);

            ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, fluid_cell_mk1)
                    .requires(gb_component)
                    .requires(fluid_housing_mk1)
                    .unlockedBy(getHasName(gb_component), has(gb_component))
                    .save(writer);
            ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, fluid_cell_mk2)
                    .requires(tb_component)
                    .requires(fluid_housing_mk2)
                    .unlockedBy(getHasName(gb_component), has(tb_component))
                    .save(writer);
        }
    }
}
