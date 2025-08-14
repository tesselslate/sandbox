package com.tesselslate.gigacells.data;

import com.tesselslate.gigacells.GigaCells;
import com.tesselslate.gigacells.GigaCellsItems;

import net.minecraft.data.DataProvider;
import net.minecraft.data.PackOutput;
import net.minecraft.world.item.Item;
import net.minecraftforge.client.model.generators.ItemModelProvider;
import net.minecraftforge.common.data.ExistingFileHelper;
import net.minecraftforge.data.event.GatherDataEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = GigaCells.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class GigaCellsModelProvider extends ItemModelProvider {
    public GigaCellsModelProvider(PackOutput output, String id, ExistingFileHelper helper) {
        super(output, id, helper);
    }

    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {
        event.getGenerator().addProvider(event.includeClient(), new DataProvider.Factory<>() {
            @Override
            public GigaCellsModelProvider create(PackOutput output) {
                return new GigaCellsModelProvider(output, GigaCells.MODID, event.getExistingFileHelper());
            }
        });
    }

    @Override
    protected void registerModels() {
        this.basicItem(GigaCellsItems.ITEM_CELL_HOUSING_MK1);
        this.basicItem(GigaCellsItems.ITEM_CELL_HOUSING_MK2);
        this.basicItem(GigaCellsItems.FLUID_CELL_HOUSING_MK1);
        this.basicItem(GigaCellsItems.FLUID_CELL_HOUSING_MK2);

        this.basicItems(GigaCellsItems.GIGABYTE_CELL_COMPONENTS);
        this.basicItems(GigaCellsItems.TERABYTE_CELL_COMPONENTS);
        this.basicItems(GigaCellsItems.GIGABYTE_ITEM_CELLS);
        this.basicItems(GigaCellsItems.TERABYTE_ITEM_CELLS);
        this.basicItems(GigaCellsItems.GIGABYTE_FLUID_CELLS);
        this.basicItems(GigaCellsItems.TERABYTE_FLUID_CELLS);
    }

    private <T extends Item> void basicItems(T[] items) {
        for (T item : items) {
            this.basicItem(item);
        }
    }
}
