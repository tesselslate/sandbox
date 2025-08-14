package com.tesselslate.gigacells.data;

import com.tesselslate.gigacells.GigaCells;
import com.tesselslate.gigacells.GigaCellsItems;

import net.minecraft.data.DataProvider;
import net.minecraft.data.PackOutput;
import net.minecraftforge.common.data.LanguageProvider;
import net.minecraftforge.data.event.GatherDataEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = GigaCells.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class GigaCellsLanguageProvider extends LanguageProvider {
    public GigaCellsLanguageProvider(PackOutput output, String id, String lang) {
        super(output, id, lang);
    }

    @Override
    protected void addTranslations() {
        this.add(GigaCellsItems.FLUID_CELL_HOUSING_MK1, "ME Advanced Fluid Cell Housing");
        this.add(GigaCellsItems.FLUID_CELL_HOUSING_MK2, "ME Advanced Fluid Cell Housing MK II");
        this.add(GigaCellsItems.ITEM_CELL_HOUSING_MK1, "ME Advanced Item Cell Housing");
        this.add(GigaCellsItems.ITEM_CELL_HOUSING_MK2, "ME Advanced Item Cell Housing MK II");

        for (int i = 0; i < 5; i++) {
            int size = 1 << (i * 2);

            this.add(GigaCellsItems.GIGABYTE_CELL_COMPONENTS[i], String.format("%dG ME Storage Component", size));
            this.add(GigaCellsItems.GIGABYTE_FLUID_CELLS[i], String.format("%dG ME Fluid Storage Cell", size));
            this.add(GigaCellsItems.GIGABYTE_ITEM_CELLS[i], String.format("%dG ME Item Storage Cell", size));

            this.add(GigaCellsItems.TERABYTE_CELL_COMPONENTS[i], String.format("%dT ME Storage Component", size));
            this.add(GigaCellsItems.TERABYTE_FLUID_CELLS[i], String.format("%dT ME Fluid Storage Cell", size));
            this.add(GigaCellsItems.TERABYTE_ITEM_CELLS[i], String.format("%dT ME Item Storage Cell", size));
        }
    }

    @SubscribeEvent
    public static void gatherData(GatherDataEvent event) {
        event.getGenerator().addProvider(event.includeClient(), new DataProvider.Factory<>() {
            @Override
            public GigaCellsLanguageProvider create(PackOutput output) {
                return new GigaCellsLanguageProvider(output, GigaCells.MODID, "en_us");
            }
        });
    }
}
