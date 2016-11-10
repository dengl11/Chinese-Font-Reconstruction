import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgSemanticModule } from "ng-semantic";
import { AppComponent } from './component_main/app.component.main';

import { MapToIterable} from './pipe/MapToIterable';


@NgModule({
    imports: [
        BrowserModule,
        NgSemanticModule,
    ],
    bootstrap: [
        AppComponent
    ],
    declarations: [
        AppComponent, 
        MapToIterable
        ]
})
export class AppModule { }
