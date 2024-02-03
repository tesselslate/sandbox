using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Monocle;
using YamlDotNet.Serialization;

namespace Celeste.Mod.WipeColor {
    [SettingName("modoptions_wipecolormodule_title")]
    public class WipeColorSettings : EverestModuleSettings {
        [SettingName("modoptions_wipecolormodule_enabled")]
        public bool ModEnabled {
            get => _Enabled;
            set {
                _Enabled = value;
                WipeColorModule.ApplyClearColor();
            }
        }

        [SettingName("modoptions_wipecolormodule_backgroundcolor")]
        [SettingSubText("Should the wipe color be applied to the background?")]
        public bool BackgroundEnabled { 
            get => _BackgroundEnabled;
            set {
                _BackgroundEnabled = value;
                WipeColorModule.ApplyClearColor();
            }
        }

        [SettingName("modoptions_wipecolormodule_applymountainwipe")]
        public bool AlwaysReplaceMountainWipe { get; set; } = false;

        [SettingName("modoptions_wipecolormodule_applyindebug")]
        [SettingSubText("Change the background of the map editor")]
        public bool ApplyToDebugMap { get; set; } = false;

        [SettingMaxLength(6)]
        [SettingName("modoptions_wipecolormodule_wipecolor")]
        [SettingSubText("The hex color to set the screen wipe to")]
        public string WipeColorString {
            get => WipeColorModule.WipeColor.R.ToString("X2") + WipeColorModule.WipeColor.G.ToString("X2") + WipeColorModule.WipeColor.B.ToString("X2");
            set {
                WipeColorModule.WipeColor = Calc.HexToColor(value);
                WipeColorModule.ApplyClearColor();

                if (WipeColorModule.StarfieldEffect != null) {
                    EffectParameter colorParam = WipeColorModule.StarfieldEffect.Parameters["WipeColor"];
                    if (colorParam != null) {
                        colorParam.SetValue(new Vector4(WipeColorModule.WipeColor.R / 255f, WipeColorModule.WipeColor.G / 255f, WipeColorModule.WipeColor.B / 255f, WipeColorModule.WipeColor.A / 255f));
                    }
                }
            }
        }



        [YamlIgnore]
        [SettingIgnore]
        private bool _BackgroundEnabled { get; set; } = true;

        [YamlIgnore]
        [SettingIgnore]
        private bool _Enabled { get; set; } = true;
    }
}